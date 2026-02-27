/**
 * 数据注册表 - 管理所有数据源和数据项
 */

import {
  DataSource,
  DataType,
  SourcedData,
  DataConflict,
  DataQuery,
  DataSourceType,
} from '../types';

interface DataStore<T> {
  byId: Map<string, SourcedData<T>>;
  bySource: Map<string, Map<string, T>>;
  index: Map<string, Set<string>>; // sourceId -> set of ids
}

export class DataRegistry {
  private sources: Map<string, DataSource> = new Map();
  private dataStores: Map<DataType, DataStore<unknown>> = new Map();
  private conflictResolution: Map<string, string> = new Map(); // dataId -> preferred sourceId

  /**
   * 注册数据源
   */
  registerSource(source: DataSource): void {
    // 检查ID冲突
    if (this.sources.has(source.id)) {
      throw new Error(`Data source with id '${source.id}' already exists`);
    }
    
    // 验证依赖
    if (source.dependencies) {
      for (const dep of source.dependencies) {
        if (!this.sources.has(dep)) {
          throw new Error(`Data source '${source.id}' depends on '${dep}' which is not registered`);
        }
      }
    }
    
    this.sources.set(source.id, source);
  }

  /**
   * 注销数据源
   */
  unregisterSource(sourceId: string): void {
    // 检查是否有其他源依赖此源
    for (const [id, source] of this.sources) {
      if (source.dependencies?.includes(sourceId)) {
        throw new Error(`Cannot unregister '${sourceId}': '${id}' depends on it`);
      }
    }
    
    // 清理数据存储
    for (const [type, store] of this.dataStores) {
      const sourceData = store.bySource.get(sourceId);
      if (sourceData) {
        for (const id of sourceData.keys()) {
          store.byId.delete(id);
        }
        store.bySource.delete(sourceId);
      }
    }
    
    this.sources.delete(sourceId);
  }

  /**
   * 启用数据源
   */
  enableSource(sourceId: string): void {
    const source = this.sources.get(sourceId);
    if (!source) {
      throw new Error(`Data source '${sourceId}' not found`);
    }
    source.enabled = true;
  }

  /**
   * 禁用数据源
   */
  disableSource(sourceId: string): void {
    const source = this.sources.get(sourceId);
    if (!source) {
      throw new Error(`Data source '${sourceId}' not found`);
    }
    source.enabled = false;
  }

  /**
   * 加载数据到注册表
   */
  loadData<T>(type: DataType, sourceId: string, data: T[]): void {
    const source = this.sources.get(sourceId);
    if (!source) {
      throw new Error(`Data source '${sourceId}' not found`);
    }

    let store = this.dataStores.get(type) as DataStore<T>;
    if (!store) {
      store = {
        byId: new Map(),
        bySource: new Map(),
        index: new Map(),
      };
      this.dataStores.set(type, store);
    }

    // 初始化源存储
    if (!store.bySource.has(sourceId)) {
      store.bySource.set(sourceId, new Map());
      store.index.set(sourceId, new Set());
    }

    const sourceMap = store.bySource.get(sourceId)!;
    const sourceIndex = store.index.get(sourceId)!;

    // 加载数据项
    for (const item of data) {
      const id = (item as unknown as { index: string }).index;
      if (!id) {
        console.warn(`Data item missing 'index' field in ${type} from ${sourceId}`);
        continue;
      }

      const sourcedData: SourcedData<T> = {
        source,
        data: item,
      };

      sourceMap.set(id, item);
      sourceIndex.add(id);

      // 检查冲突
      const existing = store.byId.get(id);
      if (existing) {
        // 记录冲突，但不覆盖（按优先级处理）
        console.debug(`Data conflict: ${type}/${id} from ${sourceId} vs ${existing.source.id}`);
      }

      // 根据优先级决定是否存储
      if (!existing || this.shouldOverride(existing.source, source)) {
        store.byId.set(id, sourcedData);
      }
    }
  }

  /**
   * 获取启用的数据源列表（按优先级排序）
   */
  getEnabledSources(): DataSource[] {
    return Array.from(this.sources.values())
      .filter(s => s.enabled)
      .sort((a, b) => b.priority - a.priority);
  }

  /**
   * 获取所有数据源
   */
  getAllSources(): DataSource[] {
    return Array.from(this.sources.values());
  }

  /**
   * 获取特定数据源
   */
  getSource(sourceId: string): DataSource | undefined {
    return this.sources.get(sourceId);
  }

  /**
   * 获取指定类型的所有活跃数据（已按优先级合并）
   */
  getActiveData<T>(type: DataType): SourcedData<T>[] {
    const store = this.dataStores.get(type);
    if (!store) {
      return [];
    }

    return Array.from(store.byId.values()) as SourcedData<T>[];
  }

  /**
   * 通过ID获取数据（自动处理优先级）
   */
  getById<T>(type: DataType, id: string): T | undefined {
    const store = this.dataStores.get(type);
    if (!store) {
      return undefined;
    }

    const sourced = store.byId.get(id);
    return sourced?.data as T;
  }

  /**
   * 通过ID和特定来源获取数据
   */
  getByIdAndSource<T>(type: DataType, id: string, sourceId: string): T | undefined {
    const store = this.dataStores.get(type);
    if (!store) {
      return undefined;
    }

    const sourceMap = store.bySource.get(sourceId);
    if (!sourceMap) {
      return undefined;
    }

    return sourceMap.get(id) as T;
  }

  /**
   * 获取特定来源的所有数据
   */
  getDataBySource<T>(type: DataType, sourceId: string): T[] {
    const store = this.dataStores.get(type);
    if (!store) {
      return [];
    }

    const sourceMap = store.bySource.get(sourceId);
    if (!sourceMap) {
      return [];
    }

    return Array.from(sourceMap.values()) as T[];
  }

  /**
   * 查询数据
   */
  query<T>(type: DataType, query: DataQuery): T[] {
    const data = this.getActiveData<T>(type);
    
    return data
      .filter(item => {
        // 应用过滤条件
        for (const [key, value] of Object.entries(query.filter || {})) {
          const itemValue = (item.data as unknown as Record<string, unknown>)[key];
          if (Array.isArray(value)) {
            if (!value.includes(itemValue as string)) return false;
          } else if (itemValue !== value) {
            return false;
          }
        }
        return true;
      })
      .map(item => item.data);
  }

  /**
   * 检测数据冲突
   */
  detectConflicts(type: DataType): DataConflict[] {
    const store = this.dataStores.get(type);
    if (!store) {
      return [];
    }

    const conflicts: DataConflict[] = [];
    const idToSources = new Map<string, string[]>();

    // 收集每个ID的来源
    for (const [sourceId, sourceMap] of store.bySource) {
      for (const id of sourceMap.keys()) {
        if (!idToSources.has(id)) {
          idToSources.set(id, []);
        }
        idToSources.get(id)!.push(sourceId);
      }
    }

    // 找出冲突
    for (const [id, sourceIds] of idToSources) {
      if (sourceIds.length > 1) {
        conflicts.push({
          type,
          id,
          sources: sourceIds.map(sid => this.sources.get(sid)!).filter(Boolean),
          currentWinner: store.byId.get(id)?.source.id,
        });
      }
    }

    return conflicts;
  }

  /**
   * 解决冲突
   */
  resolveConflict<T>(type: DataType, id: string, preferredSourceId: string): void {
    const store = this.dataStores.get(type) as DataStore<T>;
    if (!store) {
      return;
    }

    const sourceMap = store.bySource.get(preferredSourceId);
    if (!sourceMap) {
      throw new Error(`Source '${preferredSourceId}' does not have data for ${type}/${id}`);
    }

    const data = sourceMap.get(id);
    if (!data) {
      throw new Error(`Data ${type}/${id} not found in source '${preferredSourceId}'`);
    }

    const source = this.sources.get(preferredSourceId)!;
    store.byId.set(id, { source, data });
    this.conflictResolution.set(`${type}:${id}`, preferredSourceId);
  }

  /**
   * 获取数据项的来源
   */
  getDataSource<T>(type: DataType, id: string): DataSource | undefined {
    const store = this.dataStores.get(type);
    if (!store) {
      return undefined;
    }

    return store.byId.get(id)?.source;
  }

  /**
   * 检查数据是否存在
   */
  hasData(type: DataType, id: string): boolean {
    const store = this.dataStores.get(type);
    if (!store) {
      return false;
    }

    return store.byId.has(id);
  }

  /**
   * 清除所有数据
   */
  clear(): void {
    this.dataStores.clear();
    this.sources.clear();
    this.conflictResolution.clear();
  }

  /**
   * 判断新来源是否应该覆盖现有数据
   */
  private shouldOverride(existing: DataSource, incoming: DataSource): boolean {
    // 检查是否有手动冲突解决
    // 优先级高的覆盖
    return incoming.priority > existing.priority;
  }
}

// 单例实例
let globalRegistry: DataRegistry | null = null;

export function getGlobalRegistry(): DataRegistry {
  if (!globalRegistry) {
    globalRegistry = new DataRegistry();
  }
  return globalRegistry;
}

export function setGlobalRegistry(registry: DataRegistry): void {
  globalRegistry = registry;
}

// 扩展类型定义
declare module '../types' {
  interface DataQuery {
    filter?: Record<string, string | string[]>;
    sort?: { field: string; direction: 'asc' | 'desc' };
    limit?: number;
  }

  interface DataConflict {
    type: DataType;
    id: string;
    sources: DataSource[];
    currentWinner?: string;
  }
}

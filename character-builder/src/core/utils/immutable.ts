/**
 * 不可变更新工具
 * 简化版 immer 实现，用于保持状态不可变性
 */

export type Draft<T> = T extends object ? { -readonly [K in keyof T]: Draft<T[K]> } : T;

/**
 * 创建对象的不可变副本并进行修改
 */
export function produce<T>(base: T, recipe: (draft: Draft<T>) => void): T {
  // 创建深拷贝
  const draft = deepClone(base) as Draft<T>;
  
  // 应用修改
  recipe(draft);
  
  // 如果相等则返回原对象（优化）
  if (deepEqual(base, draft)) {
    return base;
  }
  
  return draft as T;
}

/**
 * 深拷贝
 */
export function deepClone<T>(obj: T): T {
  if (obj === null || typeof obj !== 'object') {
    return obj;
  }

  if (obj instanceof Date) {
    return new Date(obj.getTime()) as unknown as T;
  }

  if (Array.isArray(obj)) {
    return obj.map(item => deepClone(item)) as unknown as T;
  }

  const cloned = {} as T;
  for (const key in obj) {
    if (Object.prototype.hasOwnProperty.call(obj, key)) {
      cloned[key] = deepClone(obj[key]);
    }
  }

  return cloned;
}

/**
 * 深比较
 */
export function deepEqual(a: unknown, b: unknown): boolean {
  if (a === b) return true;
  if (typeof a !== typeof b) return false;
  if (a === null || b === null) return false;
  if (typeof a !== 'object') return false;

  if (Array.isArray(a) !== Array.isArray(b)) return false;

  if (Array.isArray(a)) {
    if ((a as unknown[]).length !== (b as unknown[]).length) return false;
    for (let i = 0; i < a.length; i++) {
      if (!deepEqual(a[i], (b as unknown[])[i])) return false;
    }
    return true;
  }

  const keysA = Object.keys(a as object);
  const keysB = Object.keys(b as object);

  if (keysA.length !== keysB.length) return false;

  for (const key of keysA) {
    if (!keysB.includes(key)) return false;
    if (!deepEqual((a as Record<string, unknown>)[key], (b as Record<string, unknown>)[key])) {
      return false;
    }
  }

  return true;
}

/**
 * 创建选择器缓存
 */
export function createSelector<T, R>(
  inputSelectors: ((state: T) => unknown)[],
  resultFunc: (...args: unknown[]) => R
): (state: T) => R {
  let lastArgs: unknown[] = [];
  let lastResult: R;

  return (state: T): R => {
    const params = inputSelectors.map(selector => selector(state));
    
    if (!shallowEqual(params, lastArgs)) {
      lastResult = resultFunc(...params);
      lastArgs = params;
    }
    
    return lastResult;
  };
}

/**
 * 浅比较
 */
function shallowEqual(a: unknown[], b: unknown[]): boolean {
  if (a.length !== b.length) return false;
  for (let i = 0; i < a.length; i++) {
    if (a[i] !== b[i]) return false;
  }
  return true;
}

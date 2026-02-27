/**
 * 平台适配层抽象
 * 为不同平台提供统一接口
 */

// 存储适配器
export interface StorageAdapter {
  get<T>(key: string): Promise<T | null>;
  set<T>(key: string, value: T): Promise<void>;
  remove(key: string): Promise<void>;
  clear(): Promise<void>;
  keys(): Promise<string[]>;
}

// 文件系统适配器
export interface FileSystemAdapter {
  readFile(path: string): Promise<Uint8Array>;
  writeFile(path: string, data: Uint8Array): Promise<void>;
  readTextFile(path: string): Promise<string>;
  writeTextFile(path: string, content: string): Promise<void>;
  exists(path: string): Promise<boolean>;
  pickFile(options?: { extensions?: string[] }): Promise<string | null>;
  pickDirectory(): Promise<string | null>;
}

// 网络适配器
export interface NetworkAdapter {
  fetch(url: string, options?: RequestInit): Promise<Response>;
  download(url: string, path?: string): Promise<Uint8Array>;
  upload(data: FormData, url: string): Promise<Response>;
}

// UI 适配器
export interface UIAdapter {
  showToast(message: string, duration?: number): void;
  showModal(options: {
    title: string;
    content: string;
    confirmText?: string;
    cancelText?: string;
  }): Promise<boolean>;
  showLoading(message?: string): void;
  hideLoading(): void;
  showPicker<T>(options: T[]): Promise<T | null>;
}

// 分享适配器
export interface ShareAdapter {
  shareText(text: string): Promise<void>;
  shareFile(path: string, mimeType: string): Promise<void>;
  shareCharacter(character: import('../types').Character, format: string): Promise<void>;
}

// 平台能力检测
export interface PlatformCapabilities {
  supportsFileSystem: boolean;
  supportsNotifications: boolean;
  supportsBackgroundSync: boolean;
  supportsOffline: boolean;
  maxStorageSize: number;
}

// 主适配器接口
export interface PlatformAdapter {
  name: string;
  version: string;
  capabilities: PlatformCapabilities;
  
  storage: StorageAdapter;
  fileSystem: FileSystemAdapter;
  network: NetworkAdapter;
  ui: UIAdapter;
  share: ShareAdapter;
  
  // 生命周期
  initialize(): Promise<void>;
  onPause?(): void;
  onResume?(): void;
  onExit?(): void;
  
  // 设备信息
  getDeviceInfo(): {
    platform: string;
    version: string;
    model?: string;
    screenWidth: number;
    screenHeight: number;
    pixelRatio: number;
  };
}

// 平台工厂
export class PlatformFactory {
  private static currentAdapter: PlatformAdapter | null = null;
  
  static setAdapter(adapter: PlatformAdapter): void {
    this.currentAdapter = adapter;
  }
  
  static getAdapter(): PlatformAdapter {
    if (!this.currentAdapter) {
      throw new Error('Platform adapter not initialized');
    }
    return this.currentAdapter;
  }
  
  static async initializeDefault(): Promise<void> {
    // 自动检测平台并初始化相应适配器
    if (typeof wx !== 'undefined') {
      // 微信小程序
      const { WXPlatformAdapter } = await import('./weixin');
      this.currentAdapter = new WXPlatformAdapter();
    } else if (typeof window !== 'undefined') {
      // Web 环境
      const { WebPlatformAdapter } = await import('./web');
      this.currentAdapter = new WebPlatformAdapter();
    } else {
      throw new Error('Unable to detect platform');
    }
    
    await this.currentAdapter.initialize();
  }
}

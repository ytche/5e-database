/**
 * Web 平台适配器
 */

import {
  PlatformAdapter,
  StorageAdapter,
  FileSystemAdapter,
  NetworkAdapter,
  UIAdapter,
  ShareAdapter,
  PlatformCapabilities,
} from '../platform-adapter';

// LocalStorage 实现
export class LocalStorageAdapter implements StorageAdapter {
  async get<T>(key: string): Promise<T | null> {
    try {
      const value = localStorage.getItem(key);
      if (value === null) return null;
      return JSON.parse(value) as T;
    } catch {
      return null;
    }
  }

  async set<T>(key: string, value: T): Promise<void> {
    localStorage.setItem(key, JSON.stringify(value));
  }

  async remove(key: string): Promise<void> {
    localStorage.removeItem(key);
  }

  async clear(): Promise<void> {
    localStorage.clear();
  }

  async keys(): Promise<string[]> {
    return Object.keys(localStorage);
  }
}

// IndexedDB 实现（大容量存储）
export class IndexedDBAdapter implements StorageAdapter {
  private dbName = 'CharacterBuilderDB';
  private storeName = 'data';
  private db: IDBDatabase | null = null;

  private async getDB(): Promise<IDBDatabase> {
    if (this.db) return this.db;

    return new Promise((resolve, reject) => {
      const request = indexedDB.open(this.dbName, 1);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => {
        this.db = request.result;
        resolve(this.db);
      };
      
      request.onupgradeneeded = (event) => {
        const db = (event.target as IDBOpenDBRequest).result;
        if (!db.objectStoreNames.contains(this.storeName)) {
          db.createObjectStore(this.storeName);
        }
      };
    });
  }

  async get<T>(key: string): Promise<T | null> {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      const request = store.get(key);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result ?? null);
    });
  }

  async set<T>(key: string, value: T): Promise<void> {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      const request = store.put(value, key);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async remove(key: string): Promise<void> {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      const request = store.delete(key);
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async clear(): Promise<void> {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readwrite');
      const store = transaction.objectStore(this.storeName);
      const request = store.clear();
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve();
    });
  }

  async keys(): Promise<string[]> {
    const db = await this.getDB();
    return new Promise((resolve, reject) => {
      const transaction = db.transaction([this.storeName], 'readonly');
      const store = transaction.objectStore(this.storeName);
      const request = store.getAllKeys();
      
      request.onerror = () => reject(request.error);
      request.onsuccess = () => resolve(request.result as string[]);
    });
  }
}

// Web 文件系统适配器
export class WebFileSystemAdapter implements FileSystemAdapter {
  async readFile(path: string): Promise<Uint8Array> {
    const response = await fetch(path);
    const buffer = await response.arrayBuffer();
    return new Uint8Array(buffer);
  }

  async writeFile(path: string, data: Uint8Array): Promise<void> {
    // Web 环境通常不能直接写文件系统
    // 使用 File System Access API（如果可用）
    if ('showSaveFilePicker' in window) {
      const handle = await (window as unknown as { showSaveFilePicker: () => Promise<FileSystemFileHandle> }).showSaveFilePicker();
      const writable = await handle.createWritable();
      await writable.write(data);
      await writable.close();
    } else {
      // 回退到下载
      const blob = new Blob([data]);
      const url = URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = path;
      a.click();
      URL.revokeObjectURL(url);
    }
  }

  async readTextFile(path: string): Promise<string> {
    const response = await fetch(path);
    return response.text();
  }

  async writeTextFile(path: string, content: string): Promise<void> {
    await this.writeFile(path, new TextEncoder().encode(content));
  }

  async exists(path: string): Promise<boolean> {
    try {
      const response = await fetch(path, { method: 'HEAD' });
      return response.ok;
    } catch {
      return false;
    }
  }

  async pickFile(options?: { extensions?: string[] }): Promise<string | null> {
    return new Promise((resolve) => {
      const input = document.createElement('input');
      input.type = 'file';
      if (options?.extensions) {
        input.accept = options.extensions.map(ext => `.${ext}`).join(',');
      }
      input.onchange = () => {
        const file = input.files?.[0];
        resolve(file ? URL.createObjectURL(file) : null);
      };
      input.click();
    });
  }

  async pickDirectory(): Promise<string | null> {
    // File System Access API
    if ('showDirectoryPicker' in window) {
      const handle = await (window as unknown as { showDirectoryPicker: () => Promise<FileSystemDirectoryHandle> }).showDirectoryPicker();
      return handle.name;
    }
    return null;
  }
}

// Web 网络适配器
export class FetchNetworkAdapter implements NetworkAdapter {
  async fetch(url: string, options?: RequestInit): Promise<Response> {
    return fetch(url, options);
  }

  async download(url: string): Promise<Uint8Array> {
    const response = await fetch(url);
    const buffer = await response.arrayBuffer();
    return new Uint8Array(buffer);
  }

  async upload(data: FormData, url: string): Promise<Response> {
    return fetch(url, {
      method: 'POST',
      body: data,
    });
  }
}

// Web UI 适配器
export class WebUIAdapter implements UIAdapter {
  private loadingElement: HTMLElement | null = null;

  showToast(message: string, duration = 3000): void {
    // 创建 toast 元素
    const toast = document.createElement('div');
    toast.className = 'toast-message';
    toast.textContent = message;
    toast.style.cssText = `
      position: fixed;
      bottom: 20px;
      left: 50%;
      transform: translateX(-50%);
      background: rgba(0, 0, 0, 0.8);
      color: white;
      padding: 12px 24px;
      border-radius: 4px;
      z-index: 10000;
      font-size: 14px;
    `;
    
    document.body.appendChild(toast);
    
    setTimeout(() => {
      toast.remove();
    }, duration);
  }

  async showModal(options: {
    title: string;
    content: string;
    confirmText?: string;
    cancelText?: string;
  }): Promise<boolean> {
    return new Promise((resolve) => {
      const backdrop = document.createElement('div');
      backdrop.style.cssText = `
        position: fixed;
        top: 0;
        left: 0;
        right: 0;
        bottom: 0;
        background: rgba(0, 0, 0, 0.5);
        display: flex;
        align-items: center;
        justify-content: center;
        z-index: 10000;
      `;

      const modal = document.createElement('div');
      modal.style.cssText = `
        background: white;
        border-radius: 8px;
        padding: 24px;
        max-width: 400px;
        width: 90%;
      `;

      modal.innerHTML = `
        <h3 style="margin: 0 0 16px 0;">${options.title}</h3>
        <p style="margin: 0 0 24px 0; color: #666;">${options.content}</p>
        <div style="display: flex; justify-content: flex-end; gap: 12px;">
          <button id="modal-cancel" style="padding: 8px 16px;">${options.cancelText || '取消'}</button>
          <button id="modal-confirm" style="padding: 8px 16px;">${options.confirmText || '确认'}</button>
        </div>
      `;

      backdrop.appendChild(modal);
      document.body.appendChild(backdrop);

      const confirmBtn = modal.querySelector('#modal-confirm') as HTMLButtonElement;
      const cancelBtn = modal.querySelector('#modal-cancel') as HTMLButtonElement;

      confirmBtn.onclick = () => {
        backdrop.remove();
        resolve(true);
      };

      cancelBtn.onclick = () => {
        backdrop.remove();
        resolve(false);
      };

      backdrop.onclick = (e) => {
        if (e.target === backdrop) {
          backdrop.remove();
          resolve(false);
        }
      };
    });
  }

  showLoading(message = '加载中...'): void {
    if (this.loadingElement) {
      this.hideLoading();
    }

    this.loadingElement = document.createElement('div');
    this.loadingElement.style.cssText = `
      position: fixed;
      top: 0;
      left: 0;
      right: 0;
      bottom: 0;
      background: rgba(255, 255, 255, 0.8);
      display: flex;
      flex-direction: column;
      align-items: center;
      justify-content: center;
      z-index: 10000;
    `;

    this.loadingElement.innerHTML = `
      <div style="
        width: 40px;
        height: 40px;
        border: 4px solid #f3f3f3;
        border-top: 4px solid #3498db;
        border-radius: 50%;
        animation: spin 1s linear infinite;
      "></div>
      <p style="margin-top: 16px; color: #666;">${message}</p>
      <style>
        @keyframes spin {
          0% { transform: rotate(0deg); }
          100% { transform: rotate(360deg); }
        }
      </style>
    `;

    document.body.appendChild(this.loadingElement);
  }

  hideLoading(): void {
    if (this.loadingElement) {
      this.loadingElement.remove();
      this.loadingElement = null;
    }
  }

  async showPicker<T>(options: T[]): Promise<T | null> {
    // 简化实现，实际应该使用更复杂的 UI
    const result = prompt(
      '请选择:\n' + options.map((o, i) => `${i + 1}. ${String(o)}`).join('\n'),
      '1'
    );
    
    if (result === null) return null;
    
    const index = parseInt(result, 10) - 1;
    return options[index] ?? null;
  }
}

// Web 分享适配器
export class WebShareAdapter implements ShareAdapter {
  async shareText(text: string): Promise<void> {
    if (navigator.share) {
      await navigator.share({ text });
    } else {
      // 回退到剪贴板
      await navigator.clipboard.writeText(text);
      alert('已复制到剪贴板');
    }
  }

  async shareFile(path: string, mimeType: string): Promise<void> {
    // Web 分享文件比较复杂，通常需要用户交互
    console.log('Share file:', path, mimeType);
  }

  async shareCharacter(character: import('../../types').Character, format: string): Promise<void> {
    const shareData: ShareData = {
      title: `D&D 角色卡 - ${character.name}`,
      text: `查看我的D&D角色: ${character.name}`,
    };

    if (navigator.share) {
      await navigator.share(shareData);
    } else {
      await this.shareText(JSON.stringify(character, null, 2));
    }
  }
}

// Web 平台主适配器
export class WebPlatformAdapter implements PlatformAdapter {
  name = 'Web';
  version = '1.0.0';
  
  capabilities: PlatformCapabilities = {
    supportsFileSystem: 'showSaveFilePicker' in window,
    supportsNotifications: 'Notification' in window,
    supportsBackgroundSync: 'serviceWorker' in navigator && 'sync' in ServiceWorkerRegistration.prototype,
    supportsOffline: 'serviceWorker' in navigator,
    maxStorageSize: 50 * 1024 * 1024, // 50MB (estimate for IndexedDB)
  };

  storage: StorageAdapter;
  fileSystem: FileSystemAdapter;
  network: NetworkAdapter;
  ui: UIAdapter;
  share: ShareAdapter;

  constructor() {
    // 使用 IndexedDB 作为主要存储
    this.storage = new IndexedDBAdapter();
    this.fileSystem = new WebFileSystemAdapter();
    this.network = new FetchNetworkAdapter();
    this.ui = new WebUIAdapter();
    this.share = new WebShareAdapter();
  }

  async initialize(): Promise<void> {
    // 注册 Service Worker（如果支持）
    if ('serviceWorker' in navigator) {
      try {
        await navigator.serviceWorker.register('/sw.js');
      } catch (err) {
        console.warn('Service Worker registration failed:', err);
      }
    }
  }

  getDeviceInfo() {
    return {
      platform: navigator.platform,
      version: navigator.userAgent,
      screenWidth: window.screen.width,
      screenHeight: window.screen.height,
      pixelRatio: window.devicePixelRatio,
    };
  }
}

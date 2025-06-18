class EventChannel {
  private target = new EventTarget();

  on(event: string, callback: (data: any) => void, ...filterPorts: string[]) {
    this.target.addEventListener(event, (e: Event) => {
      const payload = (e as CustomEvent).detail;
      const targetPort = payload?.port;

      if (
        !!targetPort &&
        filterPorts.length > 0 &&
        !filterPorts.includes(targetPort)
      )
        return;
      const data = payload?.data;
      callback(data);
    });
  }

  off(event: string, callback?: (data: any) => void) {
    this.target.removeEventListener(event, callback as EventListener);
  }

  emit(event: string, data?: any, port?: string) {
    this.target.dispatchEvent(
      new CustomEvent(event, { detail: { data, port } })
    );
  }
}
export default new EventChannel();
export class EventRadio<TData> extends EventChannel {
  private channel: string = "";

  constructor(channel: string) {
    super();
    this.channel = channel;
  }

  transmit = (data: TData, targetPort?: string) => {
    this.emit(this.channel, data, targetPort);
    return this;
  };

  listen = (callback: (data: TData) => void, ...filterPorts: string[]) => {
    this.on(this.channel, callback, ...filterPorts);
    return this;
  };

  disconnect = (callback?: (data: TData) => void) => {
    this.off(this.channel, callback);
    return this;
  };
}

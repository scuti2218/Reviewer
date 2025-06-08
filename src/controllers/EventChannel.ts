class EventChannel {
  private target = new EventTarget();

  on(event: string, callback: (payload: any) => void) {
    this.target.addEventListener(event, (e: Event) => {
      callback((e as CustomEvent).detail);
    });
  }

  off(event: string, callback?: (payload: any) => void) {
    this.target.removeEventListener(event, callback as EventListener);
  }

  emit(event: string, payload?: any) {
    this.target.dispatchEvent(new CustomEvent(event, { detail: payload }));
  }
}
export default new EventChannel();
export class EventRadio<TData> {
  private channel: string = "";
  private eventChannel: EventChannel = new EventChannel();

  constructor(channel: string) {
    this.channel = channel;
  }

  transmit = (data: TData) => this.eventChannel.emit(this.channel, data);
  listen = (callback: (data: TData) => void) =>
    this.eventChannel.on(this.channel, callback);
  disconnect = (callback?: (data: TData) => void) =>
    this.eventChannel.off(this.channel, callback);
}

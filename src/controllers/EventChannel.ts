class EventChannel {
  private target = new EventTarget()

  on(event: string, callback: (payload: any) => void) {
    this.target.addEventListener(event, (e: Event) => {
      callback((e as CustomEvent).detail)
    })
  }

  off(event: string, callback: (payload: any) => void) {
    this.target.removeEventListener(event, callback as EventListener)
  }

  emit(event: string, payload?: any) {
    this.target.dispatchEvent(new CustomEvent(event, { detail: payload }))
  }
}

export default new EventChannel()
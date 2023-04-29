class Queue {
  q: Array<any>;
  constructor() {
    this.q = [];
  }
  send(item: any) {
    this.q.push(item);
  }
  receive() {
    return this.q.shift();
  }
  queue() {
    return this.q;
  }
}

export { Queue };

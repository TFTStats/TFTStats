var Queue = /** @class */ (function () {
    function Queue() {
        this.q = [];
    }
    Queue.prototype.send = function (item) {
        this.q.push(item);
    };
    Queue.prototype.receive = function () {
        return this.q.shift();
    };
    return Queue;
}());
export { Queue };

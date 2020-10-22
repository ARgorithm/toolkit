## Priority Queue

> ARgorithmToolkit.PriorityQueue

Methods Supported

| Method | Parameters      | Description                                              | example        |
| ------ | --------------- | -------------------------------------------------------- | -------------- |
| Peek   |                 | returns first element of priority queue                  | pq.peek()      |
| Poll   |                 | pops and returns first element of priority queue         | pq.poll()      |
| Offer  | element : `any` | add element to priority queue                            | pq.offer(elem) |
| Empty  |                 | returns boolean indicating whether queue is empty or not | pq.empty()     |

Example

```python
>>> import ARgorithmToolkit
>>> algo = ARgorithmToolkit.StateSet()
>>> pq = ARgorithmToolkit.PriorityQueue('pq',algo,comments="declaring priority queue")
>>> pq.offer(9)
>>> pq.offer(3)
>>> pq.offer(7)
>>> len(pq)
3
>>> pq.peek("peeking the queue")
3
>>> pq.poll()
3
>>> len(pq)
2
>>> pq.peek()
7
>>> pq.empty()
False
```


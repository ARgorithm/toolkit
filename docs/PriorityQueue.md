## Priority Queue

> ARgorithmToolkit.PriorityQueue

Methods Supported

| Method | Parameters      | Description                                              |
| ------ | --------------- | -------------------------------------------------------- |
| Peek   |                 | returns first element of priority queue                  |
| Poll   |                 | pops and returns first element of priority queue         |
| Offer  | element : `any` | add element to priority queue                            |
| Empty  |                 | returns boolean indicating whether queue is empty or not |

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


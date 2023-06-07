# Testing Frameworks

### Here are the examples of using web frameworks that are closest to real tasks.

Testing was carried out using [wrk](https://github.com/wg/wrk).

Before the tests, you should run the command, first substituting the user ID instead of "user_id":

```shell
export USER_ID=user_id
```

1. [BlackSheep](https://github.com/Neoteroi/BlackSheep) is an asynchronous web framework to build event based web applications with Python.

   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8001/user?user_id=${USER_ID}"
   ```

   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8001/user?user_id=c0909032-cca6-4158-8435-aece30386960
     4 threads and 64 connections
     Thread Stats   Avg      Stdev     Max   +/- Stdev
       Latency     7.84ms    3.32ms  29.09ms   52.42%
       Req/Sec     2.06k   224.72     2.69k    66.83%
     Latency Distribution
        50%    7.53ms
        75%   10.78ms
        90%   12.06ms
        99%   14.93ms
     122811 requests in 15.03s, 36.89MB read
   Requests/sec:   8171.15
   Transfer/sec:      2.45MB
   ```
2. [Litestar](https://github.com/litestar-org/litestar) is a powerful, performant, flexible and opinionated ASGI framework, offering first class typing support and a full Pydantic integration.

   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8002/user/${USER_ID}"
   ```

   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8002/user/c0909032-cca6-4158-8435-aece30386960
     4 threads and 64 connections
     Thread Stats   Avg      Stdev     Max   +/- Stdev
       Latency    10.81ms    4.92ms  34.32ms   48.13%
       Req/Sec     1.49k   150.68     1.80k    66.50%
     Latency Distribution
        50%    9.46ms
        75%   15.86ms
        90%   17.44ms
        99%   21.47ms
     89023 requests in 15.03s, 26.74MB read
   Requests/sec:   5921.30
   Transfer/sec:      1.78MB
   ```
3. [FastAPI](https://github.com/tiangolo/fastapi) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
   
   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8000/api/user/${USER_ID}"
   ```
   
   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8000/api/user/c0909032-cca6-4158-8435-aece30386960
     4 threads and 64 connections
     Thread Stats   Avg      Stdev     Max   +/- Stdev
       Latency    16.65ms    8.04ms  61.11ms   58.77%
       Req/Sec     0.97k   192.00     1.22k    69.17%
     Latency Distribution
        50%   17.82ms
        75%   22.38ms
        90%   24.87ms
        99%   41.75ms
     58250 requests in 15.04s, 17.50MB read
   Requests/sec:   3872.99
   Transfer/sec:      1.16MB
   ```

## Docs
* BlackSheep: [Swagger](http://localhost:8001/docs#/)
* Litestar: [Swagger](http://localhost:8002/schema/swagger#/), [ReDoc](http://localhost:8002/schema/redoc#/)
* FastAPI: [Swagger](http://localhost:8000/api/openapi#/)

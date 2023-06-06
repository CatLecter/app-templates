# Testing Frameworks

### Here are the examples of using web frameworks that are closest to real tasks.

1. [BlackSheep](https://github.com/Neoteroi/BlackSheep) is an asynchronous web framework to build event based web applications with Python.

   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8001/user?user_id={user_id}"
   ```

   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8001/user?user_id=260793b4-e4b1-4237-82cc-0937c5d74380
      4 threads and 64 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    31.21ms   17.21ms  73.64ms   46.99%
        Req/Sec   515.10    348.17     1.96k    89.33%
      Latency Distribution
         50%   26.31ms
         75%   48.39ms
         90%   51.42ms
         99%   62.65ms
      30788 requests in 15.04s, 9.13MB read
    Requests/sec:   2046.73
    Transfer/sec:    621.61KB
   ```
2. [Litestar](https://github.com/litestar-org/litestar) is a powerful, performant, flexible and opinionated ASGI framework, offering first class typing support and a full Pydantic integration.

   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8002/user/{user_id}"
   ```

   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8002/user/260793b4-e4b1-4237-82cc-0937c5d74380
      4 threads and 64 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    34.16ms   20.49ms 110.65ms   59.79%
        Req/Sec   474.17    330.49     1.34k    78.83%
      Latency Distribution
         50%   35.06ms
         75%   50.22ms
         90%   63.28ms
         99%   78.03ms
      28340 requests in 15.03s, 8.41MB read
    Requests/sec:   1885.36
    Transfer/sec:    572.61KB
   ```
3. [FastAPI](https://github.com/tiangolo/fastapi) is a modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
   
   <span style="color: #FF7276" >Input:<span/>

   ```shell
   wrk -d15s -t4 -c64 --latency "http://localhost:8000/api/user/{user_id}"
   ```
   
   <span style="color: #FF7276" >Output:<span/>

   ```text
   Running 15s test @ http://localhost:8000/api/user/260793b4-e4b1-4237-82cc-0937c5d74380
      4 threads and 64 connections
      Thread Stats   Avg      Stdev     Max   +/- Stdev
        Latency    79.14ms   19.16ms 202.00ms   82.00%
        Req/Sec   202.45     55.85   720.00     95.67%
      Latency Distribution
         50%   81.30ms
         75%   89.58ms
         90%   97.62ms
         99%  134.66ms
      12109 requests in 15.06s, 3.59MB read
    Requests/sec:    804.28
    Transfer/sec:    244.27KB
   ```

## Docs
* BlackSheep: [Swagger](http://localhost:8001/docs#/)
* Litestar: [Swagger](http://localhost:8002/schema/swagger#/), [ReDoc](http://localhost:8002/schema/redoc#/)
* FastAPI: [Swagger](http://localhost:8000/api/openapi#/)

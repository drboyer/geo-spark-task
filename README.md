# geo-spark-task

Toy Spark jobs used to test running a PySpark task with an externally
defined dependency using the Kubernetes backend.

Note that pyspark is not yet supported in the Kubernetes backend
in Spark 2.3.0, so you'll have to stick with the [forked version](https://github.com/apache-spark-on-k8s/spark) instead.

## running it

```sh
bin/spark-submit \
  --deploy-mode cluster \
  --master k8s://https://<k8s-apiserver-host>:<k8s-apiserver-port> \
  --kubernetes-namespace <k8s-namespace> \
  --conf spark.executor.instances=2 \
  --conf spark.app.name=spark-pi \
  --conf spark.kubernetes.driver.docker.image=drboyer/geo-spark-task-driver:latest \
  --conf spark.kubernetes.executor.docker.image=drboyer/geo-spark-task-executor:latest \
  --jars local:///opt/spark/examples/jars/spark-examples_2.11-2.2.0-k8s-0.5.0.jar \
  local:///opt/spark/work-dir/pointcount.py
```

Fill in your k8s namespace (like `default`) and cluster connection point in the `--master` param

## building it

```sh
docker build -t drboyer/geo-spark-task-driver -f Dockerfile-master .
docker build -t drboyer/geo-spark-task-executor -f Dockerfile-executor .
docker push drboyer/geo-spark-task-driver
docker push drboyer/geo-spark-task-executor
```

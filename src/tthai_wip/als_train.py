from pyspark.sql import SparkSession
from pyspark.sql.types import StructType, StructField, StringType, IntegerType, FloatType

# Initialize Spark
spark = SparkSession.builder.appName("NetflixALS").getOrCreate()

# Define schema
schema = StructType([
    StructField("CustomerID", IntegerType(), False),
    StructField("MovieID", IntegerType(), False),
    StructField("Rating", FloatType(), False)
])

# Load data
ratings_df = spark.read.schema(schema).csv("file:///home/tthai2004/dataset/rating_matrix/part-00000")
ratings_df.show(5)

# Cache for performance
ratings_df.cache()

from pyspark.ml.recommendation import ALS
from pyspark.ml.evaluation import RegressionEvaluator

# Split data (80% train, 20% test)
(train_df, test_df) = ratings_df.randomSplit([0.8, 0.2], seed=42)

# Configure ALS
als = ALS(
    maxIter=10,
    regParam=0.1,
    userCol="CustomerID",
    itemCol="MovieID",
    ratingCol="Rating",
    coldStartStrategy="drop",
    nonnegative=True
)

# Train model
model = als.fit(train_df)

# Predict on test set
predictions = model.transform(test_df)
predictions.show(5)

# Evaluate with RMSE
evaluator = RegressionEvaluator(
    metricName="rmse",
    labelCol="Rating",
    predictionCol="prediction"
)
rmse = evaluator.evaluate(predictions)
print(f"Root Mean Squared Error: {rmse}")

# Recommend top-5 movies for all users
user_recs = model.recommendForAllUsers(5)
user_recs.show(5, truncate=False)

# Join with movie titles
movies_df = spark.read.csv("file:///home/tthai2004/dataset/subset_netflix/subset_movie_titles.txt", schema=StructType([
    StructField("MovieID", IntegerType(), False),
    StructField("YearOfRelease", IntegerType(), True),
    StructField("Title", StringType(), True)
]))
user_recs_exploded = user_recs.selectExpr("CustomerID", "explode(recommendations) as rec").select("CustomerID", "rec.MovieID", "rec.rating")
recs_with_titles = user_recs_exploded.join(movies_df, "MovieID").select("CustomerID", "MovieID", "Title", "rating")
recs_with_titles.show(5)

# debug
'''
movies_df.printSchema()
movies_df.show()
user_recs_exploded.select("MovieID").distinct().show(10)
movies_df.select("MovieID").distinct().show(10)
'''
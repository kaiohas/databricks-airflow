# Databricks notebook source
from pyspark.sql.functions import to_date, round, first, col 


# COMMAND ----------

#dbutils.fs.rm("dbfs:/databricks-results/prata",True)
#display(dbutils.fs.ls("dbfs:/databricks-results/prata"))

# COMMAND ----------

df_junto = spark.read.parquet("dbfs:/databricks-results/bronze/*/*/*")

# COMMAND ----------

moedas = ['USD','EUR','GBP']

# COMMAND ----------

df_moedas = df_junto.filter(df_junto.moeda.isin(moedas))

# COMMAND ----------

df_moedas = df_moedas.withColumn("data",to_date("data"))

# COMMAND ----------

resulta_taxas_conversao = df_moedas.groupBy("data")\
                                    .pivot("moeda")\
                                    .agg(first("taxa"))\
                                    .orderBy("data",ascending=False)


# COMMAND ----------

resultado_valores_reais = resulta_taxas_conversao.select("*")

# COMMAND ----------

for moeda in moedas:
     resultado_valores_reais = resultado_valores_reais.withColumn(moeda, round(1/col(moeda),4))



# COMMAND ----------

resulta_taxas_conversao = resulta_taxas_conversao.coalesce(1)
resultado_valores_reais = resultado_valores_reais.coalesce(1)

# COMMAND ----------

resulta_taxas_conversao.write\
    .mode("overwrite")\
    .format("csv")\
    .option("header","true")\
    .save("dbfs:/databricks-results/prata/taxas_conversao")


resultado_valores_reais.write\
    .mode("overwrite")\
    .format("csv")\
    .option("header","true")\
    .save("dbfs:/databricks-results/prata/valores_reais")

# COMMAND ----------



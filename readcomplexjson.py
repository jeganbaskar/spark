
import findspark
findspark.init()
from pyspark.sql import SparkSession,types

spark = SparkSession.builder.master("local").appName('Json File')\
                    .getOrCreate()
					
input_df=spark.read.json('input2.json', multiLine=True)
input_df1=spark.read.json('input1.json', multiLine=True)
input_df1.printSchema()

input_df.schema['Education']
from pyspark.sql.types import *
from pyspark.sql.functions import col,lit,struct

def flatten_struct(schema, prefix=""):
    result = []
    for elem in schema:
        if isinstance(elem.dataType, StructType):
            result += flatten_struct(elem.dataType, prefix + elem.name + ".")
           # result.replace("Column<b","")
        else:
            result.append(col(prefix + elem.name).alias(prefix + elem.name))
    return result

l1=flatten_struct(input_df.schema)
l2=flatten_struct(input_df1.schema)

list1=[]
list2=[]
for i in l1:
    list1.append(str(i).split("`")[1])
    
for i in l2:
    list2.append(str(i).split("`")[1])
	
	
from pyspark.sql.types import *
chk=set(list2)-set(list1)
for i in chk:
    if i.find("."):
        colm=i.split(".")[0]
        colm_new=i.split(".")[1]
        s_fields = input_df.schema[colm].dataType.names
        s_type=input_df1.schema[colm].dataType[colm_new].dataType
                
        in_df=input_df.withColumn(colm,
                            struct(*([col(colm)[c].alias(c) for c in s_fields] +
                                     [lit("null").cast(s_type).alias(colm_new)]
                                     ))
                                 )
        s_fields = sorted(in_df.schema[colm].dataType.names)
        
        in_df=in_df.withColumn(colm,
                            struct(*([col(colm)[c].alias(c) for c in s_fields] ))
                                 )	
								 
in_df.printSchema()

out_df=in_df.union(input_df1)
out_df.show()

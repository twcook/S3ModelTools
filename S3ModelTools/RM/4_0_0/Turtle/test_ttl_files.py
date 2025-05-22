import sys 

from pyshacl import validate

r = validate('s3mcjff70c8904bblzl3ujhclwu0.ttl',
      shacl_graph='s3model_4_0_0_Shapes.ttl',
      ont_graph='s3model_4_0_0.ttl',
      inference='rdfs',
      abort_on_error=False,
      meta_shacl=True,
      advanced=True,
      js=False,
      debug=False)
conforms, results_graph, results_text = r

print('============')
print('============')
print('============')
stdoutOrigin=sys.stdout 
sys.stdout = open("output_graph.ttl", "w")
print('Results Graph: ', '/n', results_graph)
print('============')

sys.stdout = open("results.txt", "w")

print('Results Text: ', results_text)
sys.stdout.close()
sys.stdout=stdoutOrigin
print('============')
print('Conforms: ', conforms)

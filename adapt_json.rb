file_name = "networkx_graph_data.json"
text = File.read(file_name)
text = text.gsub("'", '"')
text = text.gsub(': False', ': "False"')
File.open(file_name, "w") { |file| file.puts text}
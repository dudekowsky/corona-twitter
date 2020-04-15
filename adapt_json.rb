file_names = ["networkx_graph_data.json", "networkx_small_graph_data.json"]
file_names.each do |file_name|
	text = File.read(file_name)
	text = text.gsub("'", '"')
	text = text.gsub(': False', ': "False"')
	File.open(file_name, "w") { |file| file.puts text}
end
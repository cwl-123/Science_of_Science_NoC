% program name:citation_network
% program_discription: Constructing the mapping relationship of the nodes (paper_id,lable,year)
% and edges(source,target,type,id,weight) of the citation network.
% input:references.csv
% output:edges.csv,nodes.csv

references=readcell('reference.csv');
[length,width]=size(references);
edges=cell(1,5);
nodes=cell(length,3);

% generate nodes.csv
nodes(1,:)={'paper_id','label','year'};
for i=2:length
    nodes{i,1}=references{i,1};
    nodes{i,2}=references{i,1};
    nodes{i,3}=references{i,2};
end
xlswrite('result (gephi import file)/nodes.csv',nodes);

% generate edges.csv
edges(1,:)={'Source','Target','Type','Id','Weight'};
now_site=2;
for i=2:length
    for j=3:width
       if ~strcmp(class(references{i,j}),'missing')
           edges{now_site,1}=references{i,1};%Source
           edges{now_site,2}=references{i,j};%Target
           edges{now_site,3}='Directed';%Type
           edges{now_site,4}=now_site-1;%Id
           edges{now_site,5}=1;%Weight
           now_site=now_site+1;
       end
    end
end
xlswrite('result (gephi import file)/edges.csv',edges);

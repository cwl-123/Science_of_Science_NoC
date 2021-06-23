% program name:subject_citation_network
% program_discription: Constructing the mapping relationship of the nodes (paper_id,lable,year)
% and edges(source,target,type,id,weight,year) of the subject citation network.
% input:edges(citation_network).csv,relation.xls
% output:edges.csv,nodes.csv

citation_edges=readcell('edges(citation_network).csv');
relation=readcell('relation.xlsx');
result=citation_edges(:,[1,2,3,5]);
result{1,5}='year';

%% for edges.csv (source,target,type,weight,year)
% change the paper_id to topic
for i=2:length(citation_edges)
%   Until both two nodes in an edge are successfully matched in relation, we can replace it with topic(subject). 
    node1_ismatch=0;
    node2_ismatch=0;
    
    for j=2:length(relation)
        if citation_edges{i,1}==relation{j,1}
        node1_ismatch=1;
        node1_topic=relation{j,2};
        year=relation{j,3};
        end
    end
    
    for k=2:length(relation)
        if citation_edges{i,2}==relation{k,1}
        node2_ismatch=1;
        node2_topic=relation{k,2};
        end
    end
    
    if node1_ismatch==1&&node2_ismatch==1
        result{i,1}=node1_topic;
        result{i,2}=node2_topic;
        result{i,5}=year;
    end
end

% Separate the topics, put a starting topic and a destination topic on one line
topic_edges=cell(length(result),5);
result_length=length(result);
topic_edges(1,:)={'Source','Target','Type','weight','year'};
now_site=2;
for l=2:result_length
    if ~isempty(result{l,1})&& ~isempty(result{l,2})
    S1 = regexp(result{l,1}, ",", 'split');
    S2 = regexp(result{l,2}, ",", 'split');
    S1_length=length(S1);
    S2_length=length(S2);
    for q=1:S1_length
        for w=1:S2_length
            if ~isempty(S1{1,q})&&~isempty(S2{1,w})
             topic_edges{now_site,1}=S1{1,q};
             topic_edges{now_site,2}=S2{1,w};
             topic_edges{now_site,3}=result{l,3};
             topic_edges{now_site,4}=result{l,4};
             topic_edges{now_site,5}=result{l,5};
             now_site=now_site+1;
            end
    end
end
    end
end
xlswrite('result (gephi import file)/edges.csv',topic_edges);

%% for nodes.csv  (paper_id,lable,year)
newedges=" ";
for u=2:length(topic_edges)
   newedges(u-1,1)=strtrim(topic_edges{u,1});
   newedges(u-1,2)=strtrim(topic_edges{u,2});
end
new_nodes=unique(newedges);

% search for the first year of topics
% first init all the year as 2020
nodes=cell(length(new_nodes)+1,3);
nodes(1,:)={'paper_id','lable','year'};
for i=2:length(nodes)
   nodes{i,3}=2020;
   nodes{i,1}=new_nodes(i-1);
   nodes{i,2}=new_nodes(i-1);
end
%search for ture year of topics
for i=2:length(nodes)
    now_year=nodes{i,3};
    for j=2:length(topic_edges)
        if ~isempty(topic_edges{j,1})&&~isempty(nodes{i,1})
      if strcmp( nodes{i,1},topic_edges{j,1})
          now_year=min(now_year,topic_edges{j,5});%取两者较小的那个作为起始年份
      end
        end
    end
     for j=2:length(topic_edges)
         if ~isempty(topic_edges{j,2})&&~isempty(nodes{i,1})
      if strcmp( nodes{i,1},topic_edges{j,2})
          now_year=min(now_year,topic_edges{j,5});
      end
         end
     end
     nodes{i,3}=now_year;
end
xlswrite('result (gephi import file)/nodes.csv',nodes);











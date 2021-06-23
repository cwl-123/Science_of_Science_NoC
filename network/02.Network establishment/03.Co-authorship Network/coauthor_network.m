% program name:coauthor_network
% program_discription: Constructing the mapping relationship of the nodes (Id,label,weight,year)
% and edges(source,target,year) of the Co-authorship network.
% sub_task:get the weight and the year of authors
% input:year_id_authors.xlsx,
% output:nodes.csv, edges.csv

record=readcell('year_id_authors.xlsx');
edges=cell(length(record),3);
edges(1,:)={'source','target','year'};
[r_length,r_width]=size(record);

%% build for edges.csv (source,target,year)
now_site=2;
for i=2:r_length
    if ~isempty(record{i,4})% indicate that there are at least two authors for this paper
    for j=3:r_width
        for k=(j+1):r_width
            if ~strcmp(class(record{i,j}),'missing')&&~strcmp(class(record{i,k}),'missing')
                edges{now_site,1}=record{i,j};
                edges{now_site,2}=record{i,k};
                edges{now_site,3}=record{i,1};
                now_site=now_site+1;
            end
        end
     end
    end
end
xlswrite('result (gephi import file)/edges.csv',edges);

%% build for nodes.csv (Id,label,weight,year)
% get base nodes
[len_edges,wid_edges]=size(edges);
newedges=" ";
for u=2:len_edges
   newedges(u-1,1)=strtrim(edges{u,1});
   newedges(u-1,2)=strtrim(edges{u,2});
end
tmp_nodes=unique(newedges);

% unit base nodes.csv
nodes=cell(length(tmp_nodes)+1,4);
nodes(1,:)={'Id','Label','Weight','Year'};
for i=2:length(nodes)
   nodes{i,1}=tmp_nodes(i-1);
   nodes{i,2}=tmp_nodes(i-1);
   nodes{i,3}=0;
   nodes{i,4}=2020;
end

% add_year
for i=2:length(nodes)
    now_year=nodes{i,4};
    for j=2:length(edges)
        if ~isempty(edges{j,1})&&~isempty(nodes{i,1})
      if strcmp( nodes{i,1},edges{j,1})
          now_year=min(now_year,edges{j,3});%get the min of the two year
      end
        end
    end
     for j=2:length(edges)
         if ~isempty(edges{j,2})&&~isempty(nodes{i,1})
      if strcmp( nodes{i,1},edges{j,2})
          now_year=min(now_year,edges{j,3});
      end
         end
     end
     nodes{i,4}=now_year;
end

% add_author_weight
for i=3:r_width
    for j=2:r_length
        for g=2:length(nodes)
        if strcmp(record{j,i},nodes{g,1})
            nodes{g,3}=nodes{g,3}+1/(i-2);
        end
        end
    end
end
xlswrite('result (gephi import file)/nodes.csv',nodes);




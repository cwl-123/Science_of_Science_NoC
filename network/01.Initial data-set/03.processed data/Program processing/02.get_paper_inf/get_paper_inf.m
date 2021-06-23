%program_name:get_paper_inf 
%program_discription:to sort out information of paper
%input: new_relation.xls,citation_year.xlsx,papers.xlsx
%output: paper_info.xlsx

result=cell(length(new_relation),5);
result{1,1}='paper_id';
% read data from excel
new_relation=readcell('new_relation');
xls_1=xlsread('citation_year');
target=xls_1(:,2);
id_title=readcell('papers.xlsx');

result{1,2}='title';
result{1,3}='year';
result{1,4}='topic';
result{1,5}='cited_count';


for i=2:length(new_relation)
    cited_count=0;
    title='';
    for j=1:length(target)
        if new_relation{i,1}==target(j)
            cited_count=cited_count+1;
        end
    end
    for k=2:length(id_title)
        if id_title{k,1}==new_relation{i,1}
            title=id_title{k,2};
        end
    end
result{i,1}=new_relation{i,1};
result{i,2}=title;
result{i,3}=new_relation{i,3};
result{i,4}=new_relation{i,2};
result{i,5}=cited_count;
end
xlswrite('paper_info.xlsx',result)



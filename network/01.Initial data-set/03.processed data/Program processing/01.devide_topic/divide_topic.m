%program_name:divide_topic
%This program solves the problem of converting the paper-subjects 
%relationship into a one-to-one correspondence
%input: relation.xls
%output: new_relation.xls

%The length of new_relation is temporarily set to length(relation), 
%and it will be dynamically expanded and increased later
relation=readcell('relation');
new_relation=cell(length(relation),3);

new_relation{1,1}='paper_id';
new_relation{1,2}='topic';
new_relation{1,3}='year';

now_site=2;
for i=2:length(relation)
    if ~isempty(relation{i,2})
    S=regexp(relation{i,2}, ",", 'split');
    for j=1:length(S)
        if ~isempty(S(j))
        new_relation{now_site,1}=relation{i,1};
        new_relation{now_site,2}=S(j);
        new_relation{now_site,3}=relation{i,3};
        now_site=now_site+1;
        end
    end
    end
end

b=[new_relation{:}];
b=reshape(b,length(b)/3,3);
xlswrite('new_relation.xls',b)


% program name:new_authors_with_subjects
% program_discription: What new fields(subjects) are new authors entering
% input:relation.xls
% output:author_subjects.csv (author,year,paper_id,topic)

relation=readcell('new_relation.xls');
author_inf=readcell('author_inf.xlsx');
res=cell(1,4);
res(1,:)={'author','year','paper_id','topic'};

now_site=2;i=2;
while i<length(author_inf)
    res{now_site,1}=author_inf{i,3};
    res{now_site,2}=author_inf{i,2};
    res{now_site,3}=author_inf{i,1};
    while 1
        if strcmp(author_inf{i,3},author_inf{i+1,3})
            if(author_inf{i+1,2}<author_inf{i,2})
                res{now_site,2}=author_inf{i+1,2};
                res{now_site,3}=author_inf{i+1,1};
            end
            i=i+1;
        else 
            i=i+1;
            now_site=now_site+1;
            break;
        end
    end
end

for j=2:length(res)
    paper_id=res{j,3};
    sign=4;
    for k=2:length(relation)
        if(paper_id==relation{k,1})
            res{j,sign}=relation{k,2};
            sign=sign+1;
        end
    end
end
xlswrite('new_author_with_subjects.csv',res);




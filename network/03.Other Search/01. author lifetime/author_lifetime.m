% program name:author_lifetime
% program_discription: Calculate the lifetime for each
% author.(author_name,start year,end_year,lifetime)
% input:author_inf.xlsx
% output:author_lifetime.csv

record=readcell('author_inf.xlsx');
res=cell(1,4);
res(1,:)={'author_name','start year','end_year','lifetime'};
now_site=2;i=2;
while i<length(record)
     res{now_site,1}=record{i,3};
     res{now_site,2}=record{i,2};
     res{now_site,3}=record{i,2};
while 1
    if strcmp(record{i,3},record{i+1,3})&&i<length(record)
        res{now_site,2}=min(record{i+1,2},res{now_site,2});
        res{now_site,3}=max(record{i+1,2},res{now_site,3});
        i=i+1;
    else
        res{now_site,4}=res{now_site,3}-res{now_site,2}+1;
        now_site=now_site+1;
        i=i+1;
        break
    end
end
end
xlswrite('author_lifetime.csv',res);




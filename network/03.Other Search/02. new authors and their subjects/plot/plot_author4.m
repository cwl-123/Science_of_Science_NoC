   A =[
 
74	6	0	6	4	0	23	30	21	24
89	5	0	14	7	6	8	15	15	16
61	5	2	8	4	2	5	17	23	13
48	12	5	7	8	5	9	1	11	13
37	18	17	11	8	6	7	9	10	8
54	9	19	8	15	4	10	24	13	5

];

    A=reshape(A,[6 1 10]);
    x={2015,2016,2017,2018,2019,2020} ;
    plotBarStackGroups(A,x);
    set(gca,'FontSize',24); 
    xlabel('year','FontName','Times New Roman','FontSize',36);
    ylabel('number of new authors','FontName','Times New Roman','FontSize',36);
    h=legend( 'others',	'Routing',	'NoC for SiP','NoC for different applications',  	'router design',	'Design space Exploration',	'NoC for memory',	'topology',	'emerging technology',	'flow control' );

    set(h,'FontName','Times New Roman','FontSize',24,'FontWeight','normal')
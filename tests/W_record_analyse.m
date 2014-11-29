close all

f=figure();
subplot(1,1,1);

%name='L1_record.txt';
name='W_record.txt'
W=load(name);


hold on
W(1,4)=0;
plot(W(:,1),W(:,2),'-');
a=axis()

index=W(:,3)==1

plot(W(index,1),W(index,2),'or');
index=~index;
plot(W(index,1),W(index,2),'ob');

xlabel('t')
ylabel('W')
% plot(W(:,1),W(:,4),'x');

a(2)=25000
axis(a);

%subplot(1,2,2);
%name='L2_record.txt'
%W=load(name);   

% title(name);
% hold on
% W(1,4)=0;
% plot(W(:,1),W(:,2),'-');
% a=axis()
% 
% index=W(:,3)==1
% 
% plot(W(index,1),W(index,2),'or');
% index=~index;
% plot(W(index,1),W(index,2),'ob');

% plot(W(:,1),W(:,4),'x');

axis(a);

set(f,'Position',[200,200,800,400]);
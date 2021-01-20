function []= Safe_Time(critical_temp)

    load Air.dat;
    TR = 8.63/2 *2.54/100;      %Tank radius
    OR = (TR + 1*2.54/100);     %Insulation radius

    %OT = outer tempertaure of insulation 
    OT = 283;
    env_temp = 310;
    L = 17*2.54/100;
    k = 0.033;          %Cond coeff of styrofoam
    emiss = 0.05;
    stephboltz = 5.67 * 10^(-8);
    m=25.46;                    %mass of tank in kg
    C=502.416;                  %Specific heat of steel in J/kgK

    hconv = CylNuT(2,OR*2,Air,OT);
    hrad = emiss*stephboltz*(OT^2 + env_temp^2)*(OT + env_temp);
    Rcondc = log(OR./TR)./(2*pi*L*k);
    Rconvc = 1./(2*pi*OR*L*hconv);
    Rradc = 1./(hrad*2*pi*OR*L);
    Rcyl = 1./(1./Rconvc +1./Rradc) + Rcondc;

    Rconds = (1./TR - 1./OR)./(4*pi*k);
    Rconvs = 1./(2*pi*OR^2 *hconv);
    Rrads = 1./(2*pi*OR^2 * hrad);
    Rsphere = 1./(1./Rconvs +1./Rrads) +Rconds;
    
    Rnet = (Rcyl*Rsphere)./(2*Rcyl +Rsphere);
    
    tank_temp=77.36; %starting temperature of tank
    t=0;             %Initial time =0
    dt=0.1;          %time step
    
    while tank_temp < critical_temp
         tempDiff = (env_temp - tank_temp);
         heatflow = (tempDiff / Rnet);
         dQ=heatflow*dt;
         tank_temp=dQ./(m*C)+tank_temp;
         t=t+dt;
    end
    disp(t)

    


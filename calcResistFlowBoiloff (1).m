function calcResistFlowBoiloff()

    thickn = input("What is the insulation thickness (in In)? ")
    ambTemp = input("What is the ambient temperature (in K)? ")
    liq = input("What is the liquid inside the tank? ", 's')


    disp("Total Resistance:")

    totalResistance = total_resistance(thickn, ambTemp, liq)

    %ct = cryo temp / innter tem
    
    if liq == "methane"
            CT = 111.7; %Boiling point of methane
        elseif liq == "oxygen"
            CT = 90.19; %BP of oxygen
        elseif liq == "nitrogen"
            CT = 77.36; %BP of nitrogen
        else
            error("Please input either methane, oxygen, or nitrogen.")
    end
    
    tempDiff = (ambTemp - CT);
    
    disp("Heat Flow in W")
    heatFlow = calcHeatFlow(totalResistance, tempDiff)
    disp(hconv)
    disp("Boil Off Rate in lbm/hr")
    boilOff = calcBoiloff(heatFlow, liq)
    
    




 function Rnet = total_resistance(thickness,ambient_temperature,liquid)



    load Air.dat;
    TR = 8.63/2 *2.54/100;
    OR = (TR + thickness*2.54/100);

    %OT = outer temp 
    
    if liquid == "nitrogen" 
            OT = 310.928; %OT, outer surface temperature assume dessert temperature for insulation
    else 
            OT = 283; %assume post chill down for lox and methane
    end

    env_temp = ambient_temperature;
    L = 17*2.54/100;
    k = 0.033;
    emiss = 0.05;
    stephboltz = 5.67 * 10^(-8);

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




function heatFlow = calcHeatFlow(totalResistance, tempDiff)


heatFlow = (tempDiff / totalResistance);



function boilOff = calcBoiloff(heatFlow, liq)

%note to self - ask prof how to calculate boil off (heat of vaporization?)

     if liq == "methane"
            hVap = 511283.2893; %hvap of methane in j/kg
        elseif liq == "oxygen"
            hVap = 213132.0708; %hvap of oxygen
        elseif liq == "nitrogen"
            hVap = 199390.2918; %hvap of nitrogen
     end    
     
     boilOffRateInKgPerSec = heatFlow / hVap;
     
     boilOff = boilOffRateInKgPerSec * 3600 * 2.20462;
     
     
    

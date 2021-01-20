

#return minor loss value (k) of pipe from water test. 

library(readxl)

########################################## input data ######################################################################


#data <- read_excel("Path where your Excel file is stored\\File Name.xlsx",sheet = "Your sheet name")


#########################################initialize vlaue from water test. ###################################################


p.total <- NULL + 14.7 # total pressure of system. Includes dynamic and static pressures. Given values from pump in psig.Values +- unknown. Sig figs unknown.
p.error <- 2
p.sig <- 3

flow.rate <- NULL #given mass flow rate. Values +- 2%. Three sig figs.
flow.error <- 2
flow.sig <- 3
rho <- 0.99802 #denisty of water g/cm^3
d <- .5
r <- d/2 #cross-sectional radius of tubing, inches
k0 <- (1-.5^2/2^2)^2 #minor loss contraction (punp -> hose) coefficient. Source: https://web2.clarkson.edu/projects/subramanian/ch330/notes/Minor%20Losses.pdf
v <- flow.rate/(pi*r^2)
epsilon <- NULL #relative roughness check errors 
epsi.error <- 2
epsi.sig <- 3
viscosity <- 0.0008900#viscosity of water
length <- NULL #length of pipe. check error w / hoalin


################################################ calculate k ######################################################################


#find dynap to seperatetotal pressure
get.dynap <- function (rho,v){
  dynap <- .5*rho*v^2
  return (dynap)
}

get.re <- function (rho,visco,v,d){
  re <-1/visco*rho*v*d
  return (re)
}

#Zigrang and Sylvester approximation to get darcy friction factor
#max error < .13%
get.friction <- function (epsi,re,d){
  zs <- -2*log(epsi/(3.7*d)-5.02/re*log(epsi/(3.7*d)-5.02/re*log(epsi/(3.7*d) + 13/re)))
  f <- (1/zs)^2
  return (f)
}


#get desired k value using major / minor loss formula
get.K <- function (staticp,dynamicp,friction,l,d,k0){
  K <- staticp/dynamicp - friction*(l/d)-k0
  return (K)
}






############################################ Perform Computations ####################################################
#run through functions to get k w/ error included. 
dynamicp <- get.dynap(rho,v)
staticp <- p.total - dynamicp
re <- get.re(rho,viscosity,v,2*r)
friction <- get.friction(epsilon,re,2*r)
k <- get.K(staticp,dynamicp,friction,length,2*r,k0)


#partial derivative calculated by wolfram alpha/by hand
v.error <- 1/(pi*r^2)*flow.error
dynap.error <- 2*rho*v*v.error
staticp.error <- ((dynap.error)^2+p.error^2)^0.5
re.error <- 1/(viscosity*rho*v^2*2*r)*v.error
friction.error <- re.error*4.36*d*(-2.18*d*(-5.646*d-log((0.27*epsilon*re+13*d)/(d*re))*(0.27*epsilon*re+13*d))-log((0.37*epsilon*re-5.02*d*log((.27*epsilon*re+13*d)/(d*re)))/(d*re))*(0.27*epsilon*re+13*d)*(0.37*epsilon*re-5.02*d*log(13/re+.27*epsilon/d)))/(re*(0.27*epsilon*re+13*d)*(0.27*epsilon*re-5.02*d*log(13/re+.27*epsilon/d))*(0.27*epsilon*re-5.02*d*log(0.27*epsilon/d-5.02*log(0.27*epsilon/d+13/re)/re)))
k.error <- ((1/dynamicp*staticp.error)^2+(staticp/dynamicp^2*dynap.error)^2+(friction.error/d)^2)^0.5 
#addd sig figs when get an actual answer for error / k
print(k)
print(k.error)







  
  
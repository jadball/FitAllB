import numpy as n
import check_input
import write_output
import reject
import fit
import fcn
import time
import minuit
import sys
import logging
from copy import deepcopy
logging.basicConfig(level=logging.DEBUG,format='%(levelname)s %(message)s')


class fit_minuit():
    def __init__(self,inp):
        self.inp = inp
        
			
    def refine(self):	
	"""
	Carry out one refinement cycle according to the order given by self.inp.fit['reforder']
	Reject reflection according to self.inp.fit['rej_resmean']
	Print and save refinement and rejection info and parameters
	
	Jette Oddershede, Risoe DTU, May 15 2008
	"""
		
        # initialise
        self.poor_value = []
        self.poor_nrefl = []

 		# create lists of parameters, global and for each grain
        self.globals = ["wx","wy","tx","ty","tz","py","pz","cy","cz","L"]
        self.grains = []
        for i in range(self.inp.no_grains):
            self.grains.append(["x%s" %i,"y%s" %i,"z%s" %i,"rodx%s" %i,"rody%s" %i,"rodz%s" %i,
                                "epsaa%s" %i,"epsbb%s" %i,"epscc%s" %i,"epsbc%s" %i,"epsac%s" %i,"epsab%s" %i])

        #refinement update
        reload(fcn)
        self.m = minuit.Minuit(fcn.FCN)
        self.m.values = self.inp.values
        self.m.errors = self.inp.errors
        for entries in self.m.fixed:
            self.m.fixed[entries] = True

		# determine whether to refine
        self.ref = False
        if 'globals' in self.inp.fit['goon']:
            self.ref = True
		

		# carry out refinement
        if self.ref == True:
            self.mg = minuit.Minuit(fcn.FCNgrain)
            self.mg.values = self.m.values
            self.mg.errors = self.m.errors
            self.mg.fixed = self.m.fixed

            print '\n\n*****Now fitting %s*****' %self.inp.fit['goon']
            print 'newreject_grain', self.inp.fit['newreject_grain']
            # calculate starting values
            g = fit.grain_values(self)
            self.fval = sum(g)
            print '\n%s starting value %e' %(self.inp.fit['goon'],self.fval)
            t1 = time.clock()
            self.fitglobals()
            print 'Fit %s tolerance %e' %(self.inp.fit['goon'],self.m.tol)
            self.m.errors = self.inp.errors
            self.m.migrad()
            fit.scale_errors(self)
            self.inp.values = self.m.values
            self.inp.errors = self.m.errors
            write_output.write_global(self)
				
            self.time = time.clock()-t1
            print 'Fit %s time %i s' %(self.inp.fit['goon'],self.time)
            print 'Fit %s value %e \n' %(self.inp.fit['goon'],self.m.fval)
			    
			
            # reject outliers and save cycle info	
            fit.reject_outliers(self)
            write_output.write_rej(self.inp,message=self.inp.fit['goon'])
            write_output.write_log(self)
            write_output.write_par(self)

		# move onto next refinement given by the reforder list	
        self.inp.fit['goon'] = self.inp.fit['reforder'][self.inp.fit['reforder'].index(self.inp.fit['goon'])+1]

        return
        
        
    def fitglobals(self):
	"""
	Set tolerance and fixed parameters for preliminary fit of the global parameters
	"""
        self.m.tol = self.inp.fit['tol_global']
        self.mg.tol = self.m.tol
        for entries in self.m.fixed:
            if entries=='wy' and self.inp.fit['w'] != 0:
                self.m.fixed[entries] = False
            elif entries[0]=='t' and self.inp.fit['tilt'] != 0:
                self.m.fixed[entries] = False
            elif 'p' in entries and len(entries) == 2 and self.inp.fit['pixel'] != 0:
                self.m.fixed[entries] = False
            elif entries=='cy' and self.inp.fit['center'] != 0:
                self.m.fixed[entries] = False
            elif 'L' in entries and self.inp.fit['L'] != 0:
                self.m.fixed[entries] = False

		
def refine(inp):
    while inp.fit['goon'] != 'end':
        check_input.set_globals(inp)
        # build functions to minimise
        from FitAllB import build_fcn
        build_fcn.FCN(inp)
        # minuit fitting
        from FitAllB import fitga
        lsqr = fitga.fit_minuit(inp)
        lsqr.refine()
        check_input.copy_globals(inp)
   
   

					

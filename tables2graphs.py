#genera los graficos para la presentacion para los indios a partir de las tablas del reporte en latex
#por cada evaluador se grafican 4 graficos por cada aspecto: svm, rf, rf texto y rf todo

import matplotlib.pyplot as plt
import sys
import numpy as np

#input del tipo:
# \textit{Arithmetic} &6.16&7.52&0&0&8.65&7.96\\\hline
# \textit{Equations} &9.6&8.93&4.16&7.51&1.91&13.64\\\hline
# \textit{Statistics} &0.76&0.76&7.18&9.53&24.45&17.19\\\hline
# \textit{Fractions} &3.7&3.63&1.69&0.97&0&0\\\hline
# \textit{Geometry} &10.81&7.89&0.63&0.63&15.43&8.81\\\hline
# \textit{Analytic Geometry} &0&0&0.97&0.68&9&2.86\\\hline
# \textit{Proportio- nality} &4.1&7.76&3.39&4.86&19.79&15.48\\\hline
# \textit{Algebra} &4.41&1.76&18.76&13.92&25&21.65\\\hline
# \textit{Dynamics} &14.04&8.22&4.23&2.69&2.34&4.99\\\hline
# \textit{Instruction} &8.05&7.62&6.02&4.88&12.73&8.99\\\hline
# \textit{Interpella- tion} &20.19&8.08&14.12&5.95&18.07&9.4\\\hline
# \textit{Positive Valuation} &8.19&8.07&0&0&5.21&8.24\\\hline
# \textit{Negative Valuation} &0&0&1.9&0.94&1.01&1\\\hline
# \textit{Phatic} &6.53&7.77&9.84&4.99&21.65&9.78\\\hline
# \textit{Explana- tion} &17.33&8.07&10.15&5.73&27.65&9.93\\\hline
# \textit{Metaphor} &4.7&7.07&13.8&13.24&30.36&27.27\\\hline
# \textit{Reasoning} &9.08&6.77&1.17&2.75&2.17&1.52\\\hline
# \textit{Computa- tion} &0.78&6.75&2.95&3.8&16.25&9.39\\\hline
# \textit{Reinforce- ment} &15.8&8.12&1.43&3.35&1.05&1.05\\\hline
# \textit{Classifica- tion} &0&0&2.39&1.06&0&0\\\hline

#recibe el nombre del archivo de la lista de archivos como argumento
filename = sys.argv[1]

#una variable que guarde los nombres de los aspectos, una para los nombres de los metodos y una para los evaluadores
aspects = ['Arithmetic', 'Equations', 'Statistics', 'Fractions', 'Geometry', 'Analytic Geometry', 'Proportionality', 'Algebra', 
'Dynamics', 'Instruction', 'Interpellation', 'Positive Valuation', 'Negative Valuation', 'Phatic', 'Explanation', 'Metaphor', 
'Reasoning', 'Computation', 'Reinforcement', 'Classification']
nAspects = len(aspects)

methods = ['svm-music', 'rf-music', 'rf-text', 'rf-text+music']
nMethods = len(methods)

raters = ['Taecher1', 'Teacher2', 'Mathematician2']
nRaters = len(raters)

#dos arreglos de aspectos por metodos por evaluadores. Una con los ks y la otra con los errores
ks = np.empty([nAspects, nMethods, nRaters])
err = np.empty([nAspects, nMethods, nRaters])

#indices de aspecto y metodo
iAspect = 0
iMethod = 0

#abre el archivo
with open(filename, 'r') as f:
	#por cada linea se abre el archivo correspondiente a un metodo (una tabla)
	for tablefile in f.readlines():
		tablefile = tablefile.replace('\n', '')
		with open(tablefile, 'r') as t:
			#por cada linea
			for row in t.readlines():
				row = row.replace('\n', '')
				row = row.replace('\\', '')
				row = row.replace('hline', '')
				row = row.split('&')
				row = [float(item) for item in row[1:]]
				#obtiene el aspecto y los valores y se agregan a la variable correspondiente
				ks[(iAspect, iMethod, 0)] = row[0]
				err[(iAspect, iMethod, 0)] = row[1]
				ks[(iAspect, iMethod, 1)] = row[2]
				err[(iAspect, iMethod, 1)] = row[3]
				ks[(iAspect, iMethod, 2)] = row[4]
				err[(iAspect, iMethod, 2)] = row[5]
				iAspect += 1
		iMethod += 1
		iAspect = 0	
#se grafican las variables
nPlots = 4

ind = np.arange(nPlots)    # the x locations for the groups
width = 0.2       # the width of the bars: can also be len(x) sequence

for i in xrange(nRaters):

	p1 = plt.bar(0, width, ks[ind,0,i], ind, color='b', xerr=err[ind,0,i], ecolor='k', orientation='horizontal')
	p2 = plt.bar(0, width, ks[ind,1,i], ind+width, color='r', xerr=err[ind,1,i], ecolor='k', orientation='horizontal')
	p3 = plt.bar(0, width, ks[ind,2,i], ind+2*width, color='g', xerr=err[ind,2,i], ecolor='k', orientation='horizontal')
	p4 = plt.bar(0, width, ks[ind,3,i], ind+3*width, color='y', xerr=err[ind,3,i], ecolor='k', orientation='horizontal')

	plt.xlabel('KS')
	plt.xlim(0,100)
	plt.xticks(np.arange(0,101,10))
	plt.yticks(ind+2*width, np.array(aspects)[ind], rotation=17)
	plt.suptitle('KS by aspect and method for ' + raters[i], fontsize=15)
	plt.legend( (p1[0], p2[0], p3[0], p4[0]), methods , 'lower right' )
	plt.savefig('./graphs/' + raters[i] + '.png')
	plt.close()
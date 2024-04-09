# Python program for DDA line generation 

from matplotlib import pyplot as plt 

# DDA Function for line generation 


def DDA(x0, y0, x1, y1): 

	# find absolute differences 
	dx = abs(x0 - x1) 
	dy = abs(y0 - y1) 

	# find maximum difference 
	steps = max(dx, dy) 

	# calculate the increment in x and y 
	xinc = dx/steps 
	yinc = dy/steps 

	# start with 1st point 
	x = float(x0) 
	y = float(y0) 

	# make a list for coordinates 
	x_coorinates = [x] 
	y_coorinates = [y] 

	for i in range(steps): 
		# append the x,y coordinates in respective list 
		 

		# increment the values 
		x = x + xinc 
		y = y + yinc
		
		x_coorinates.append(round(x)) 
		y_coorinates.append(round(y))
	print(x_coorinates)
	print(y_coorinates)
	# plot the line with coordinates list 
	plt.plot(x_coorinates, y_coorinates, marker="o", 
			markersize=5, markerfacecolor="black") 
	plt.show() 


# Driver code 
if __name__ == "__main__": 

	# coordinates of 1st point 
	x0, y0 = 0, 0

	# coordinates of 2nd point 
	x1, y1 = 4, 6

	# Function call 
	jp = DDA(x0, y0, x1, y1) 
	print(jp)

	# This code is contributed by 111arpit1 

"""
Module of functions that recolor a target image based on
a reference image. Recolors TARGET_IMAGE to approximate
TARGET_COLORS as much as possible to REFERENCE_COLORS.

Attributes:
target_image -- image whose colors will be updated
target_colors -- colors that represent the palette of target_image.
reference_colors -- colors to which target_colors must approximate.

Returns:
recolored_image -- image whose colors are as close as possible to those of reference_colors
"""

import numpy as np
import cv2

from functions.color import Color

def rgb_weighted_average(target_image, target_colors, reference_colors):
	"""
	Uses reference RGB color to approximate color with cluster
	colors as weights of a weighted average.
	"""

	Color.load_cluster()

	rate = 0
	rate_count = 1

	color_weights_total = np.array([0., 0., 0.])

	for color in ["red", "blue"]:
		if color in target_colors and color in reference_colors:
			color_index = Color.labels.index(color)
			cluster_color = Color(Color.clusters.cluster_centers_[color_index], Color.format).array("RGB")

			color_weights = cluster_color

			color_weights_total += color_weights

			rate += color_weights * reference_colors[color].array("RGB") / target_colors[color].array("RGB")
			rate_count += 1
	
	rate = rate / color_weights_total

	recolored_image = target_image * rate
	
	return recolored_image

def lab_l(target_image, target_colors, reference_colors):
	number_of_factors = 0
	for color in ["red", "blue"]:
		if color in target_colors and color in reference_colors:
			factor_total = reference_colors[color].array("LAB")[0] / target_colors[color].array("LAB")[0]

			number_of_factors += 1
	
	if number_of_factors == 0:
		return target_image
	
	factor = factor_total / number_of_factors

	lab_image = cv2.cvtColor(target_image, cv2.COLOR_BGR2LAB)

	lab_image[:,:,0] = lab_image[:,:,0] * factor

	recolored_image = cv2.cvtColor(lab_image, cv2.COLOR_LAB2BGR)

	return recolored_image

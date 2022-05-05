# BambooWork.py     Creed Jones, Virginia Tech      March 28, 2022
# In support of Dr Hauptman et al
# Bamboo reconstruction experimentation
# initial version - May 1, 2022
# Two bits of functionality are here:
# 1 - A set of images taken at equally spaced angles from 0 to 180 inclusive are input; interpolation is used to
#     build a larger set, then sinograms are extracted. The inverse radon transform is used to derive approximate
#     profiles of the bamboo at certain spaces along its length
# 2 - A single image of the bamboo is binarized, the skeleton, medial axis and distance transform of the cane is
#     extracted.

import numpy as np
import skimage
import scipy.interpolate
import matplotlib.pyplot as plt
import matplotlib.colors as colors

def createsinogram(imgs, rangelist):
    smallgram = np.mean(imgs[:, rangelist, :], axis=1)
    inputrange = [0., 45., 90., 135., 180.]
    interp = scipy.interpolate.interp1d(inputrange, smallgram, axis=0, kind='cubic')
    outrows = np.linspace(0, 180, num=256)
    sgram = interp(outrows)
    return np.transpose(sgram)

def sonogramtoslice(sgram):
    return None

def main():
    doRadon = False
    dirname = 'C:/Data/Bamboo/'
    NINPUTS = 5
    imageht = 1000
    imagewid = 250
    images = np.zeros( (NINPUTS, imageht, imagewid) )
    count = 0
    if (doRadon):
        for filename in ('38_0', '38_1', '38_2', '38_3', '38_4'):
            rawimage = skimage.io.imread(dirname+filename+'.jpg', as_gray=True)
            images[count] = rawimage[300:imageht+300, 1660:imagewid+1660]
            # skimage.io.imshow(images[count])
            # plt.show()
            count += 1
        for rangestart in [ 100, 150, 200, 250 ]:
            rangeht = 20
            rangelist = (rangestart, rangestart+rangeht)
            gram = createsinogram(images, rangelist)
            gramdisp = skimage.exposure.rescale_intensity(gram, in_range='image', out_range='uint8')
            # plt.show()
            # skimage.transform.
            result = skimage.transform.iradon(gram, interpolation='linear')
            skimage.io.imshow(result)
            palette = plt.cm.gray
            plt.show(cmap=palette)

    # now do the medial axis of the whole bamboo cane
    filename = '38_0'
    imageht = 2500
    imagewid = 250
    rawimage = skimage.io.imread(dirname+filename+'.jpg', as_gray=True)
    subimage = rawimage[300:imageht+300, 1660:imagewid+1660]
    bestthr = skimage.filters.threshold_otsu(subimage)
    binimage = subimage <= bestthr
    skeleton = skimage.morphology.skeletonize(binimage)
    medaxis, distimage = skimage.morphology.medial_axis(binimage, return_distance=True)
    distimage = np.divide(distimage, np.max(distimage))
    outimage = np.concatenate( (subimage, binimage, 1*skeleton, 1*medaxis, distimage), axis=1)
    skimage.io.imsave(dirname+filename+'_result.png', outimage)
    skimage.io.imshow(outimage)
    plt.show()
    pass
main()
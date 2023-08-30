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

import os
import numpy as np
import cv2
import skimage
import scipy.interpolate
import matplotlib.pyplot as plt

class BambooProfiler:
    def __init__(self):
        self.verbose = False
        self.dispimages = False

    def createsinogram(self, imgs):
        outimgdir = 'C:/Data/Bamboo/OutImgs/'
        anglerange = 360
        numangles = 256
        smallgramgray = np.mean(imgs, axis=1)
        smallgram = smallgramgray # 1*(smallgramgray > 0.45)
        skimage.io.imsave(outimgdir+'smallgram.png', smallgram.astype(np.ubyte))
        if (self.dispimages):
            skimage.io.imshow(smallgram), plt.show()
        anglestep = int(anglerange/(len(imgs)-1))
        inputxrange = np.arange(0, smallgram.shape[1])
        inputyrange = np.arange(0, anglerange+anglestep, anglestep)
    #    interp = scipy.interpolate.interp1d(inputyrange, smallgram, axis=0, kind='linear')
        interp = scipy.interpolate.RegularGridInterpolator(points=(inputyrange, inputxrange), values=smallgram, method='linear')
        outlimit = max(inputyrange)
        outrows = np.linspace(0, outlimit, num=numangles)
        outputxrange = np.arange(0, smallgram.shape[1])
        outputyrange = np.arange(0, numangles)
        gridx, gridy = np.meshgrid(outputyrange, outputxrange, indexing='ij')
        grid = np.stack( (gridx, gridy), axis=-1)
        gridpoints = grid.reshape(-1,2)
        rawgram = interp( gridpoints )
        sgram = rawgram.reshape( len(outrows), -1 )
        skimage.io.imsave(outimgdir+'sgram.png', sgram.astype(np.ubyte))
        # find the best midline and shift to it
        hproj = np.mean(sgram, axis=0)
        binaryproj = 1*(hproj > 0.5)
        linelen = len(binaryproj)
        leftside = np.min(np.argmin(binaryproj))
        rightside = linelen - np.min(np.argmin(np.flip(binaryproj)))
        midpoint = (leftside + rightside)/2
        delta = abs(int(linelen/2 - midpoint))
        if (midpoint < linelen/2):
            shiftedsgram = np.concatenate( (sgram[:, linelen-delta:] , sgram[:, 0:linelen-delta]), axis=1)
        else:
            shiftedsgram = np.concatenate( (sgram[:, delta:linelen] , sgram[:, 0:delta]), axis=1)
        return np.transpose(shiftedsgram)

    def sonogramtoslice(self, sgram):
        return None

    def mainTest(self):
        doRadon = True
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
            for rangestart in [ 100, 200, 300, 400, 500, 600, 700, 800, 900]:
                rangeht = 20
                rangelist = (rangestart, rangestart+rangeht)
                gram = self.createsinogram(images, rangelist)
                gramdisp = skimage.exposure.rescale_intensity(gram, in_range='image', out_range='uint8')
                # plt.show()
                result = skimage.transform.iradon(gram, interpolation='linear')
                if (self.dispimages):
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
        skimage.io.imsave(dirname+filename+'_result.png', outimage.astype(np.ubyte))
        if (self.dispimages):
            skimage.io.imshow(outimage), plt.show()
        pass

    def laserTest(self):
        dirname = 'C:/Data/Bamboo/Nov2022images/'
        filename = 'laser&white_345Degs_frame23.png'
        img = cv2.imread(dirname + filename)
        grayimg = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)[400:,:]
        # assume that 3% of the image is bright
        sorted = np.sort(grayimg.ravel())
        thrpoint = int(len(sorted)*0.98)
        thresh = sorted[thrpoint]
        thr, binaryimg = cv2.threshold(grayimg, thresh, 255, cv2.THRESH_BINARY)
        skimage.io.imshow(binaryimg), plt.show()
        pass

    def decImageTest(self):
        # dirname = 'C:/Data/Bamboo/laser_white_2/'
        dirname = 'C:/Data/Bamboo/white/'
        outimgdir = 'C:/Data/Bamboo/OutImgs/'
        filelist = self.getImageFiles(dirname)
        imageht = 1200
        imagewd = 300
        NINPUTS = len(filelist)
        images = np.zeros( (NINPUTS+1, imageht, imagewd) )
        count = 0
        for filename in filelist:
            images[count] = self.getBambooImage(dirname+filename, imageht, imagewd)
            count += 1
        # duplicate the first image as the last, so we can interpolate across 360 degrees
        images[count] = images[0]
        for rangestart in [ 100, 150, 200, 250, 300, 350, 400, 450, 500 ]:
        # for rangestart in [ 100, 150 ]:
            rangeht = 20
            rangeimgs = images[:, rangestart:rangestart+rangeht, :]
            # skimage.io.imshow(rangeimgs[0])
            palette = plt.cm.gray
            # plt.show(cmap=palette)
            gram = self.createsinogram(rangeimgs)
            gramdisp = skimage.exposure.rescale_intensity(gram, in_range='image', out_range='uint8')
            skimage.io.imsave(outimgdir + 'sonogram{}.png'.format(rangestart), gramdisp.astype(np.ubyte))
            skimage.io.imshow(gramdisp), plt.show()
            result = skimage.transform.iradon(gram, interpolation='linear')
            imgresult = self.imgnormalize(result).astype(np.ubyte)
            skimage.io.imshow(imgresult), plt.show()
            skimage.io.imsave(outimgdir + 'profile{}.png'.format(rangestart), imgresult.astype(np.ubyte))
            edgeimg = 255*skimage.feature.canny(imgresult, sigma=2.0, low_threshold=None, high_threshold=None)
            skimage.io.imshow(edgeimg), plt.show()
            skimage.io.imsave(outimgdir + 'outline{}.png'.format(rangestart), edgeimg.astype(np.ubyte))
            strelem = cv2.getStructuringElement(cv2.MORPH_RECT, 3)
            dilated = cv2.dilate(edgeimg,strelem)
            skimage.io.imshow(dilated), plt.show()
    def imgnormalize(self, img):
        MAXOUTPUT = 255.0
        MINOUTPUT = 0.0
        result = np.add( np.multiply( np.subtract(img, np.min(img.ravel())), MAXOUTPUT/(np.max(img.ravel())-np.min(img.ravel()))), MINOUTPUT)
        print(np.min(result), np.max(result))
        return result

    def getImageFiles(self, dir):
        files = os.listdir(dir)
        imgfiles = [f for f in files if f.endswith('png') or f.endswith('jpg')]
        return imgfiles

    def getBambooImage(self, pathname, imageht, imagewd):
        doClamp = False
        dirname = 'C:/Data/Bamboo/laser_white/'
        rawimage = skimage.io.imread(pathname)
        if (doClamp):
            # remove the laser line
            pixelindex = rawimage[:,:,0] > 240
            rawimage[pixelindex] = (200, 180, 150)
            skimage.io.imsave(dirname+"Clamped/clamped.png", rawimage)
        grayimage = skimage.color.rgb2gray(rawimage)
        inverted = skimage.util.invert(grayimage)
        flipped = skimage.transform.rotate(inverted, 90, resize=True)
        top = 300
        lhs = 575
        cropped = flipped[top:top+imageht, lhs:lhs+imagewd]
        return cropped


if (__name__ == "__main__"):
    # mainTest()
    # laserTest()
    BP = BambooProfiler()
    BP.decImageTest()
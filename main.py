#!/usr/bin/python

"""

Data Driven Reverb Simulator

TODO:
    Update usage()
    Read http://www.eas.uccs.edu/~mwickert/ece2610/lecture_notes/ece2610_chap8.pdf on how to solve for coefficients

"""

import os
import sys
import pdb
import time
import scipy.io.wavfile
import scipy.signal
import numpy
from util import *
from FilterNetwork import *

START_TIME=time.time()

def convert_hertz(freq, sample_rate=44100.0):
    # convert frequency in hz to units of pi rad/sample
    return freq * 2.0 / sample_rate

def usage(): 
    # Sample Usage: python main.py input.wav ./results -denoising_sigma 2
    print >> sys.stderr, ''
    print >> sys.stderr, 'Usage: python '+__file__+' input_image out_dir <options>'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Sample Usage: python '+__file__+' input.png ./results -denoising_sigma 2'
    print >> sys.stderr, ''
    print >> sys.stderr, 'EXPLANATION TEXT.'
    print >> sys.stderr, ''
    print >> sys.stderr, 'Options:'
    print >> sys.stderr, ''
    print >> sys.stderr, '    -denoising_sigma <float>'
    print >> sys.stderr, '        We first smooth the data with a Gaussian filter. The default value is 2.0.'
    print >> sys.stderr, ''
    exit(1)

def main():
    if len(sys.argv) < 3:
        usage()
    
    # Get Params
    input_wav_location = os.path.abspath(sys.argv[1])
    out_dir = os.path.abspath(sys.argv[2]) # the output directory
    makedirs(out_dir)
    denoising_sigma = float(get_command_line_param_val_default_value(sys.argv,'-denoising_sigma',2))
    
    print "Parameters: "
    print "    Input WAV File Location:",input_wav_location
    print "    Output Directory:",out_dir
    print "    Denoising Sigma:",denoising_sigma
    print 
    
    input_sample_rate, input_samples = scipy.io.wavfile.read(input_wav_location)
#    input_samples = numpy.asarray(input_samples, dtype=numpy.int16)
    output_wav_location = os.path.join(out_dir,"output.wav")
    
#    bn=1
#    b = numpy.ones(bn)/float(bn)
#    an=10000
#    a = numpy.zeros(an)
#    a[0]=1
#    a[an-1]=-0.5
#    
#    output_samples = numpy.asarray(scipy.signal.lfilter(b, a, input_samples, axis=0), dtype=numpy.int16)
#    
#    print input_samples[100:110]
#    print output_samples[100:110]
#    print output_samples[100:110]-input_samples[:10]
#    
#    scipy.io.wavfile.write(output_wav_location, input_sample_rate, output_samples)
#    
#    print 
#    print scipy.signal.lfilter(b, a, [1]+100*[0], axis=0)
    
    fn = FilterNetwork(num_layers=1, num_units_per_layer=1, num_fir_coefficients=3, num_iir_coefficients=3)
    output_code = fn.apply(input_samples)
    output_manual = numpy.asarray(scipy.signal.lfilter(fn.network[0][0][0].b, fn.network[0][0][0].a, input_samples, axis=0), dtype=numpy.int16)
    
#    print input_samples
    print "fn coefs", fn.network[0][0][0].b, fn.network[0][0][0].a
    print output_code
    print fn.final_combiner.list_of_weights
    print fn.final_combiner.list_of_weights[0]*output_manual
    
    print 
    print 'Total Run Time: '+str(time.time()-START_TIME) 
    print 

if __name__ == '__main__': 
    main() 


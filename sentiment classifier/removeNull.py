# replaces null bytes in a csv file (run once)
import sys
if len(sys.argv) < 3:
  print len(sys.argv)
  print """USAGE: python removeNull.py [input_file] [output_file]"""
  sys.exit()
  
fi = open(sys.argv[1], 'rb')
data = fi.read()
fi.close()
fo = open(sys.argv[2], 'wb')
fo.write(data.replace('\x00', '').replace('\n', ''))
fo.close()

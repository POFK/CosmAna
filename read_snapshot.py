#!/usr/bin/env python
# coding=utf-8
import numpy as np


class ReadSnapshot():
    'read data for L-Gadget'

    def __init__(self, Path=''):
        '''
        usage:
        Path='/data/dell1/userdir/maotx/output/gadget/test/snapdir_005/snapshot_005.'
        NumOfFile=64
        '''
        self.Path = Path
        self.dt = np.dtype([('head', np.int32, 1),
                            ('npart', np.int32, 6),
                            ('massarr', np.float64, 6),
                            ('time', np.float64),
                            ('redshift', np.float64),
                            ('flag_sfr', np.int32),
                            ('flag_feedback', np.int32),
                            ('npartall', np.int32, 6),
                            ('flag_cooling', np.int32),
                            ('Nsubfiles', np.int32),
                            ('BoxSize', np.float64),
                            ('Omega0', np.float64),
                            ('OmegaL', np.float64),
                            ('H', np.float64),
                            ])
        f = open(self.Path + '0', 'r')
        self.Info = np.fromfile(file=f, dtype=self.dt, count=1)
        f.close()
        self.Filenum = self.Info['Nsubfiles'][0]
#       print 'Path:', Path
#       print self.Info

    def ReadPos(self, Filenum=np.int):
        dtype_data = np.dtype([('pos', np.float32, 3)])
        f = open(self.Path + '%d' % Filenum, 'r')
        info = np.fromfile(file=f, dtype=self.dt, count=1)
        length = info['npart'][0][1]
#       print 'reading pos:'
        f.seek(self.Info['head'][0] + 4 + 4)
        a = np.fromfile(file=f, dtype=np.int32, count=1)[0]
        pos = np.fromfile(file=f, dtype=dtype_data, count=info['npart'][0][1])
        b = np.fromfile(file=f, dtype=np.int32, count=1)[0]
        f.close()
        if not (a == b and a == (length * 4 * 3)):
            print 'error in pos!'
            print a
            print b
        else:
            return pos

    def ReadVel(self, Filenum=np.int):
        dtype_data = np.dtype([('vel', np.float32, 3)])
        f = open(self.Path + '%d' % Filenum, 'r')
        info = np.fromfile(file=f, dtype=self.dt, count=1)
        length = info['npart'][0][1]
        print 'reading vel:'
        f.seek(self.Info['head'][0] + 4 + 4 + length * 4 * 3 + 4 + 4)
        a = np.fromfile(file=f, dtype=np.int32, count=1)[0]
        vel = np.fromfile(file=f, dtype=dtype_data, count=info['npart'][0][1])
        b = np.fromfile(file=f, dtype=np.int32, count=1)[0]
        f.close()
        if not (a == b and a == (length * 4 * 3)):
            print 'error in pos!'
            print a
            print b
        else:
            return vel

    def ReadPID(self, Filenum=np.int):
        f = open(self.Path + '%d' % Filenum, 'r')
        info = np.fromfile(file=f, dtype=self.dt, count=1)
        length = info['npart'][0][1]
        print 'reading PID:'
        f.seek(
            self.Info['head'][0] + 4 + 4 +
            length * 4 * 3 + 4 + 4 +
            length * 4 * 3 + 4 + 4
        )
        a = np.fromfile(file=f, dtype=np.int32, count=1)
        PID = np.fromfile(file=f, dtype=np.int64, count=info['npart'][0][1])
        b = np.fromfile(file=f, dtype=np.int32, count=1)
        f.close()
        if not (a == b and a == (length * 4 * 2)):
            print 'error in PID!'
            print a
            print b
        else:
            return PID


if __name__ == '__main__':
    import sys
    Path = sys.argv[1]
#   Path = '/data/dell1/userdir/maotx/output/gadget/test2/snapdir_005/snapshot_005.'
    NumOfFile = 64
    f = ReadSnapshot(Path)
    print f.Info
    print f.Info.dtype
'''
#========================================
    PID = []
    for i in np.arange(f.num):
        pid = f.ReadPID(Filenum=i)
        PID.append(pid)
    PID = np.hstack(PID)
#========================================
    Pos = []
    for i in np.arange(64):
        pos = f.ReadPos(Filenum=i)
        Pos.append(pos)
    Pos = np.hstack(Pos)
    Pos = np.array([i[0] for i in Pos])
#========================================
    Vel = []
    for i in np.arange(64):
        vel = f.ReadVel(Filenum=i)
        Vel.append(vel)
    Vel = np.hstack(Vel)
    Vel = np.array([i[0] for i in Vel])
'''

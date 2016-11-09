# Part 1 : Plot dielectric function with 5 periods.
mpb tri.ctl > tri.out
mpb-data -r -m 5 -n 32 tri-epsilon.h5
# h5ls tri-epsilon.h5
h5topng -S 3 tri-epsilon.h5:data-new

# Part 2 : Plot dispersion diagram & get band gap info
BAND_GAPS=$(grep Gap tri.out)
echo "Band Gaps:"
echo $BAND_GAPS
grep tmfreqs tri.out > tri-tm.dat
grep tefreqs tri.out > tri-te.dat

python plt-dispersion.py m tri-tm.dat
python plt-dispersion.py e tri-te.dat
python plt-dispersion.py c tri-te.dat tri-tm.dat

# Part 3
# Plot Ez at K point for TM Mode
mpb-data -r -m 5 -n 32 tri-e.k11.b*.z.tm.h5
h5topng -C tri-epsilon.h5:data-new -c bluered -Z -d z.r-new tri-e.k11.b*.z.tm.h5
# Plot Hz at K point for TE mode
mpb-data -r -m 5 -n 32 tri-h.k11.b*.z.te.h5
h5topng -C tri-epsilon.h5:data-new -c bluered -Z -d z.r-new tri-h.k11.b*.z.te.h5


# Part 4 : Plot magnitude of group velocity at all k-points for first two bands
grep tmvelocity tri.out > tri-tmvelocity.dat
grep tevelocity tri.out > tri-tevelocity.dat

python plt-velocity.py m tri-tmvelocity.dat
python plt-velocity.py e tri-tevelocity.dat
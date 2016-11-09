; Triangular lattice with air-holes of radius = 0.25 and epsilon = 11.56

; define r and eps as parameters
(define-param eps 11.56)
(define-param r 0.25)

(set! num-bands 4) ; Interested in first 4 bands

(set! geometry-lattice (make lattice (size 1 1 no-size)
                        (basis1 (/ (sqrt 3) 2) 0.5)
                        (basis2 (/ (sqrt 3) 2) -0.5))) ; define triangular lattice
(set! default-material (make dielectric (epsilon eps))) ; set material dielectric constant
(set! geometry (list (make cylinder
						(center 0 0 0)
						(radius r)
						(height infinity)
						(material air)
					))) ; set up cylindrical air-hole

; set k points (Bloch wavevectors) of the reciprocal-lattice space to compute bands at
(set! k-points (list (vector3 0 0 0)          ; Gamma
                     (vector3 0 0.5 0)        ; M
                     (vector3 (/ -3) (/ 3) 0) ; K
                     (vector3 0 0 0)))        ; Gamma
(set! k-points (interpolate 4 k-points)) ; interpote 16 k-points

(set! resolution 32)

(run-tm display-group-velocities (output-at-kpoint (vector3 (/ -3) (/ 3) 0)
                          fix-efield-phase output-efield-z))
(run-te display-group-velocities (output-at-kpoint (vector3 (/ -3) (/ 3) 0)
                          fix-hfield-phase output-hfield-z))

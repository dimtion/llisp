(def (bool x)
     (if (eq x 0) 0 1))

(def (! x)
     (- 1 x))

(def (and x y)
     (eq (+ (bool x) (bool y)) 2))

(def (or x y)
     (! (and (! x) (! y))))

(def (xor x y)
     (or (and x (! y)) (and (! x) y)))

(def (min x y)
     (if (< x y) x y))

(def (max x y)
     (if (< x y) y x))

(def (abs x)
     (if (< 0 x) x (- 0 x)))

(def (> x y)
     (! (< x y)))

(def (<= x y)
     (or (< x y) (eq x y)))

(def (>= x y)
     (or (> x y) (eq x y)))

(def (sqrt x)
     (var y (/ x 2))
     (def (h x y)
          (if (<= (abs (- (* y y) x)) 0.00001)
              y
              (h x (/ (+ y (/ x y)) 2))))
     (h x y))

(def (pow x y)
     (if (eq y 0)
         1
         (* x (pow x (- y 1)))))

(var pi 3.141592)

(var e 2.718281)

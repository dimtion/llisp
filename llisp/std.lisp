(def (bool x)
     (if (eq x 0) 0 1))

(def (! x)
     (- 1 (bool x)))

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

(var [] (pop (list 0)))

(def (len l)
     (if (eq l [])
     0
     (+ 1 (len (pop l)))))

(def (find e l)
     (if (eq e (el l))
         0
         (+ 1 (find e (pop l)))))

(def (reverse l)
     (def (helper l m)
          (if (eq l [])
          m
          (helper (pop l) (push (el l) m))))
     (helper l []))

(def (concat a b)
     (def (helper a b)
          (if (eq a [])
              b
              (helper (pop a) (push (el a) b))))
     (helper (reverse a) b))
     
(def (elist l)
     (if (eq l [])
      0
      ((echo (el l))
      (elist (pop l)))))

(def (chartoint s)
     (var ints (list '0' '1' '2' '3' '4' '5' '6' '7' '8' '9'))
     (def (helper s numbers)
          (if (eq s (el numbers))
              0
              (+ 1 (helper s (pop numbers)))))
     (helper s ints))

(def (toint s)
     (def (helper s)
          (if (eq s [])
             0
             (+ (chartoint (el s))
                (* 10 (helper (pop s))))))
     (helper (reverse s)))

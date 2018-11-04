(def (divide a b)
     (eq 0 (% a b)))

(def (result m a b)
     (if (eq 0 m)
         0
         (+ (if (or (divide m a) (divide m b))
                m
                0)
            (result (- m 1) a b))))

(print (result (- 1000 1) 5 3))

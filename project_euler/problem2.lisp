(def (fib n)
     (var phi (/ (+ 1 (sqrt 5)) 2))
     (// (/ (- (pow phi n) (pow (/ 1 (- 0 phi)) n)) (sqrt 5)) 1))

(def (evenfibsmall n)
     (var f (fib n))
     (if (or (> f 4000000) (eq (% f 2) 1))
         0
         f))

(def (sumfib x)
     (if (eq x 0)
         0
         (+ (evenfibsmall x) (sumfib (- x 1)))))

(var limit 34)
(print (fib limit))
(print (sumfib limit))

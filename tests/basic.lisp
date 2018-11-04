(+ 1 1)

(echo 1)

(def (fact n)
  (if (eq n 0)
      1
      (* n (fact (- n 1)))))

(echo (fact 10))

(def (hyp x y)
     (def (sum x y)
        (+ x y))
     (def (square x)
        (* x x))
     (sum (square x) (square y)))

(var triangle (hyp 5 4))
(echo triangle)



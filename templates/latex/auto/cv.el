(TeX-add-style-hook
 "cv"
 (lambda ()
   (TeX-add-to-alist 'LaTeX-provided-class-options
                     '(("moderncv" "11pt" "letter" "sans")))
   (TeX-add-to-alist 'LaTeX-provided-package-options
                     '(("geometry" "top=1in" "bottom=1in" "left=1.1in" "right=1.1in") ("biblatex" "backend=biber" "style=ieee" "defernumbers=true")))
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-braces-local "url")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "path")
   (add-to-list 'LaTeX-verbatim-macros-with-delims-local "url")
   (TeX-run-style-hooks
    "latex2e"
    "moderncv"
    "moderncv11"
    "geometry"
    "biblatex"
    "lastpage")
   (TeX-add-symbols
    "rm"
    "sf"
    "tt"
    "bf"
    "it"
    "sl"
    "sc"
    "cal"
    "mit")))


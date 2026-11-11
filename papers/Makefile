# Build all four papers. Figures and data tables are regenerated first from committed
# results, so the PDFs are always in sync with the measurements and the model.
PAPERS := paper1-signing paper2-longitudinal paper3-formal paper4-score
REPO   := ..

.PHONY: all figures data clean $(PAPERS)

all: data figures $(PAPERS)

data:
	cd $(REPO) && python3 -m mavaudit.model.report --out results/model
	cd $(REPO) && python3 -c "import json,sys; sys.path.insert(0,'.'); \
	  from mavaudit.model.synthesis import analyse; \
	  open('results/model/synthesis.json','w').write(json.dumps(analyse(),indent=2,default=list))"
	cd $(REPO) && [ -f results/longitudinal/index.json ] && \
	  python3 scripts/longitudinal_report.py || true

figures: data
	cd $(REPO) && python3 papers/common/make_figures.py

$(PAPERS):
	cd $@ && latexmk -pdf -interaction=nonstopmode -halt-on-error main.tex

clean:
	cd $(REPO) && latexmk -C papers/*/main.tex 2>/dev/null || true
	rm -f */*.aux */*.bbl */*.blg */*.log */*.out */*.fls */*.fdb_latexmk

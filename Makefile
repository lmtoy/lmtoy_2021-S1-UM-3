#


PID  = 2021-S1-UM-3
RUN1 = $(PID).run1
RUN2 = $(PID).run2

help:
	@echo PID=$(PID)
	@echo WORK_LMT=$(WORK_LMT)
	@echo Targets here:
	@echo "   runs      - make the run1/run2/... files"
	@echo "   summary   - update the project summary index"

# echo $(lmtinfo.py grep 2022 Science 2021-S1-US-3|awk '{print $2}')


$(RUN1):	mk_runs
	./mk_runs

$(RUN2):	mk_runs
	./mk_runs

runs:	$(RUN1) $(RUN2)

run1:
	@echo "Submit run1 using any of these methods:"
	@echo "    sbatch_lmtoy.sh $(RUN1)"
	@echo "    parallel --jobs 16 < $(RUN1)"
	@echo "    bash $(RUN1)"
	@echo "when this is done, run2 can be started"
run2:
	@echo submit run2 using any of these methods:
	@echo "    sbatch_lmtoy.sh $(RUN2)"
	@echo "    parallel --jobs 16 < $(RUN2)"
	@echo "    bash $(RUN2)"

summary:
	@for p in $(PID); do \
	(echo $$p;  cd $(WORK_LMT)/$$p; mk_summary1.sh > index.html); \
	done

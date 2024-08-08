# get_summary_from_functional_annotation_table
Summarize gene function annotation result tables such as Fanflow(https://github.com/bonohu/SAQE).

#### input.csv

```csv
Target-pid,XXX-ENSPID,XXX-gsymbol,XXX-gdescription,UniProtKB-ID,UniProtKB-gsymbol,UniProtKB-gdescription,YYY-ENSPID,YYY-gsymbol,YYY-gdescription,Pfam-IDs,Pfam-Names
A,XXX1,XXX_A,A protein [Source:XXX;Acc:XXXXXX],sp|AAAAA|XXXXX_YYYYY,,A protein OS=XXX OX=00000 GN=XXX PE=2 SV=1,XXX1,XXX_A,A protein [Source:XXX;Acc:XXXXXX],,
B,XXX2,XXX_B,B protein [Source:XXX;Acc:XXXXXX],sp|BBBBB|XXXXX_YYYYY,ABC,B protein OS=YYY OX=00000 GN=XXX PE=3 SV=1,XXX2,non,B protein [Source:XXX;Acc:XXXXXX],PF00000.00;  PF111111.1,AAA; BBB
C,XXX3,XXX_C,C protein [Source:XXX;Acc:XXXXXX],sp|CCCCC|XXXXX_YYYYY,,C protein  OS=YYY OX=00000 GN=XXX PE=5 SV=1,XXX3,non,non-available,PF00000.00;  PF111111.1,AAA; BBB
A,XXX4,XXX_D,D protein [Source:XXX;Acc:XXXXXX],sp|DDDDD|XXXXX_YYYYY,,D protein OS=XXX OX=00000 GN=XXX PE=1 SV=1,,,,PF00000.00;  PF111111.2,AAA; BBB
B,XXX5,XXX_E,E protein [Source:XXX;Acc:XXXXXX],sp|EEEEE|XXXXX_YYYYY,,E protein OS=XXX OX=00000 GN=XXX PE=4 SV=1,,,,PF00000.00;  PF111111.3,AAA; BBB
C,XXX6,XXX_F,F protein [Source:XXX;Acc:XXXXXX],sp|FFFFF|XXXXX_YYYYY,,,XXX6,XXX_F,non-available,PF00000.00;  PF111111.4,AAA; BBB
A,XXX7,XXX_A,A protein [Source:XXX;Acc:XXXXXX],sp|AAAAA|XXXXX_YYYYY,,A protein OS=XXX OX=00000 GN=XXX PE=2 SV=1,XXX7,XXX_A,A protein [Source:XXX;Acc:XXXXXX],PF00000.00;  PF111111.5,AAA; BBB
B,,,,,,,,,,PF00000.00;  PF111111.6,AAA; BBB
C,,,,,,,,,,PF00000.00;  PF111111.7,AAA; BBB
A,,,,,,,,,,,
```

#### Run

```bash
docker run --rm -v $(pwd):/mnt/data kazukinakamae/annotation-counter:v1.0 /mnt/data/input.csv /mnt/data/output.csv;
```

#### Output

```
Annotation category                       Annotation level      Details	                                                Detailed gene count	  Gene count
Protein homologue from tophit             Ensembl:XXX                                                                                         7
                                                                Characterized                                           7	
                                                                Less-characterized	                                    0	
                                                                Non-characterized	                                      0	
Protein homologue from tophit             Ensembl:XXX                                                                                         5
                                                                Characterized                                           2	
                                                                Less-characterized	                                    2	
                                                                Non-characterized	                                      1	
Protein homologue from tophit	            UniProtKB/Swiss-Prot			                                                                          7
                                                                XXX                                                     4	
                                                                YYY                                                     2	
                                                                Others	                                                1	
At least one of the above				                                                                                                              7
No protein homologue, but with protein domain				                                                                                          2
Total genes with protein-level annotation				                                                                                              9
Hypothetical protein				                                                                                                                  1
Total				                                                                                                                                  10
```
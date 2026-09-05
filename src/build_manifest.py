"""Authoritative shot and narration manifest. All times are seconds at 24 fps."""
import json
from pathlib import Path
ROOT = Path(__file__).resolve().parents[1]

HEART = [
('heart','Human Heart and Circulation','A journey with one red blood cell',
'इस वीडियो में हम समझेंगे Human Heart and Circulation। आपके पैर की एक cell तक oxygen कैसे पहुँचती है? यह जानने के लिए हम एक red blood cell के साथ यात्रा करेंगे। रास्ते में heart, lungs और blood vessels का काम देखेंगे।'),
('heart','The heart: a muscular pump','Four chambers · Two connected circuits',
'Heart एक muscular organ है। यह chest में lungs के बीच, थोड़ा बाईं ओर होता है। इसकी pumping से blood पूरे शरीर में घूमता है। Blood cells तक oxygen और nutrients पहुँचाता है, और carbon dioxide जैसे waste को हटाने में मदद करता है।'),
('heart_cut','Four chambers','Anatomical right appears on the left of this view',
'आइए heart को अंदर से देखें। ऊपर के दो chambers atria हैं और नीचे के दो ventricles। इस सामने वाले view में anatomical right बाईं ओर दिखाई देता है। चार chambers हैं, right atrium, right ventricle, left atrium और left ventricle।'),
('heart_cut','The septum','Separates the right and left sides',
'Right और left sides के बीच muscular partition को septum कहते हैं। सामान्य heart में यह oxygen-rich और oxygen-poor blood को अलग रखता है। Atria blood receive करते हैं। Ventricles blood को बाहर pump करते हैं। अब अपनी red blood cell का रास्ता देखें।'),
('heart_flow','Body → Right atrium','Superior and inferior vena cava',
'Body की cells को oxygen देने के बाद blood में oxygen कम और carbon dioxide अधिक होती है। यह superior और inferior vena cava से right atrium में आता है। Blue रंग कम oxygen की पहचान है। असल में यह blood भी गहरा लाल होता है।'),
('heart_flow','Right atrium → Right ventricle','Through the tricuspid valve',
'Right atrium से blood tricuspid valve के रास्ते right ventricle में जाता है। Ventricle के contraction से pressure बढ़ता है और tricuspid valve बंद हो जाता है। इससे blood atrium में वापस नहीं लौटता। Valve एक दिशा में flow बनाए रखता है।'),
('heart_flow','Right ventricle → Lungs','Pulmonary valve → Pulmonary arteries',
'Right ventricle blood को pulmonary valve से pulmonary artery में pump करता है। यह artery दोनों lungs तक जाती है। याद रखिए, artery की पहचान oxygen की मात्रा से नहीं होती। Artery वह vessel है जो blood को heart से दूर ले जाती है।'),
('alveoli','Gas exchange in the lungs','O₂ enters blood · CO₂ leaves blood',
'Lungs में capillaries, alveoli नाम के छोटे air sacs के आसपास होती हैं। पतली walls के पार oxygen, alveoli से blood में diffuse करती है। Carbon dioxide blood से alveoli में जाती है और साँस छोड़ने पर बाहर निकलती है।'),
('blood','Haemoglobin carries oxygen','Red blood cells are biconcave discs',
'Red blood cells में haemoglobin protein होता है। अधिकांश oxygen इसी से जुड़कर यात्रा करती है। Cells का बीच से पतला biconcave shape surface area बढ़ाता है और संकरी capillaries से निकलने में मदद करता है। हमारी red blood cell अब oxygen लेकर लौट रही है।'),
('heart_flow','Lungs → Left atrium','Pulmonary veins carry oxygen-rich blood',
'Oxygen-rich blood pulmonary veins से left atrium में लौटता है। इसलिए veins की पहचान भी oxygen की मात्रा से नहीं होती। Veins blood को heart की तरफ लाती हैं। Pulmonary veins में oxygen अधिक, जबकि शरीर से लौटने वाली ज्यादातर veins में कम होती है।'),
('heart_flow','Left atrium → Left ventricle','Through the mitral valve',
'Left atrium से blood mitral, या bicuspid valve के रास्ते left ventricle में जाता है। इसकी muscular wall, right ventricle से अधिक मोटी होती है। इसे blood पूरे शरीर तक पर्याप्त pressure से पहुँचाना होता है, इसलिए अधिक force की ज़रूरत होती है।'),
('heart_flow','Left ventricle → Body','Aortic valve → Aorta',
'Left ventricle contract करता है। Blood aortic valve से aorta में निकलता है। Aorta की branches पूरे शरीर तक blood पहुँचाती हैं। Heart muscle को भी oxygen चाहिए। उसकी supply के लिए aorta से coronary arteries निकलती हैं।'),
('circulation','Double circulation','Pulmonary circuit + Systemic circuit',
'पूरी यात्रा देखें। Heart से lungs और वापस heart, यह pulmonary circulation है। Heart से body tissues और वापस heart, यह systemic circulation है। एक complete circuit में blood heart से दो बार गुजरता है। इसी को double circulation कहते हैं।'),
('valve','Valves maintain one-way flow','Pressure opens and closes the leaflets',
'चार मुख्य heart valves हैं, tricuspid, pulmonary, mitral और aortic। ये pressure difference से खुलते और बंद होते हैं। Pumping heart muscle करता है। Valves का काम backward flow रोककर blood को सही दिशा में बनाए रखना है।'),
('heart_cut','The cardiac cycle','Filling → Contraction → Relaxation',
'Heart relax करके blood से भरता है। Atria का contraction ventricles की filling पूरी करता है। फिर ventricles contract करके blood बाहर भेजते हैं। Contraction को systole और relaxation को diastole कहते हैं। धीमी गति में देखें, filling, pumping और फिर relaxation।'),
('heart_cut','Why do we hear lub–dub?','Valve closure creates vibrations',
'Lub और dub मुख्य रूप से valves बंद होने की vibrations से आती हैं। पहली आवाज़ tricuspid और mitral valves के बंद होने से जुड़ी है। दूसरी आवाज़ aortic और pulmonary valves के बंद होने से जुड़ी है। यह क्रम हर heartbeat में दोहराता है।'),
('conduction','The natural pacemaker','SA node → AV node → Ventricles',
'Right atrium में SA node natural pacemaker है। उसका electrical signal atria में फैलता है। AV node पर थोड़े delay के बाद signal ventricles तक पहुँचता है। इस coordination से atria पहले और ventricles बाद में contract करते हैं।'),
('vessels','Arteries and veins','Different walls for different pressures',
'Arteries की walls मोटी, muscular और elastic होती हैं, क्योंकि इनमें pressure अधिक होता है। Veins में pressure कम और walls अपेक्षाकृत पतली होती हैं। कई veins में valves होते हैं, जो blood को पीछे बहने से रोकते हैं।'),
('capillary','Capillaries: the exchange surface','Thin walls · Short diffusion distance',
'Arteries, arterioles और फिर capillaries में बँटती हैं। Capillaries की wall मुख्यतः एक endothelial cell layer की होती है। यहाँ oxygen और nutrients tissues तक पहुँचते हैं। Carbon dioxide और दूसरे waste blood में आते हैं। पतली wall exchange को आसान बनाती है।'),
('capillary','Exchange with body cells','Diffusion follows concentration gradients',
'Oxygen को blood से tissue में जाते देखिए। Cells इसे cellular respiration में इस्तेमाल करती हैं, जिससे nutrients की energy उपयोगी रूप में मिलती है। Carbon dioxide की दिशा उलटी है। अलग substances अपने gradients और transport mechanisms के अनुसार exchange होते हैं।'),
('lymph','Lymph returns excess tissue fluid','Fluid balance · Transport · Defence',
'Tissues के बीच जमा अतिरिक्त fluid, lymphatic vessels collect करती हैं। इसे lymph कहते हैं। यह आगे veins से blood circulation में लौटता है। Lymph fluid balance, intestine से absorbed fats के transport और immune defence में मदद करती है।'),
('blood','Blood is a transport tissue','Plasma · RBCs · WBCs · Platelets',
'Blood में कई components हैं। Liquid plasma dissolved substances transport करता है। Red blood cells अधिकांश oxygen ले जाती हैं। White blood cells defence में भाग लेती हैं। Platelets damaged vessel पर clot बनने में मदद करती हैं। साथ मिलकर ये transport और protection करते हैं।'),
('circulation','Why two circuits matter','Separation supports efficient oxygen delivery',
'Double circulation से lungs और body के लिए अलग pressure बनाए रखा जा सकता है। Lungs की नाजुक capillaries के लिए कम pressure, और पूरे शरीर के लिए अधिक pressure उपयोगी है। दोनों तरह के blood का separation efficient oxygen delivery में मदद करता है।'),
('circulation','Trace the complete route','Body → Right heart → Lungs → Left heart → Body',
'यात्रा दोहराएँ। Body से vena cava, right atrium, tricuspid valve, right ventricle, pulmonary artery और lungs। फिर pulmonary veins, left atrium, mitral valve, left ventricle और aorta से body। अब आप समझ गए कि heart और blood vessels मिलकर हर cell तक उसकी ज़रूरतें कैसे पहुँचाते हैं।')]

DNA = [
('dna','DNA: From Gene to Protein','How a sequence becomes a working molecule',
'इस वीडियो में हम समझेंगे DNA से protein बनने की कहानी। Enzymes, कई hormones और structural molecules proteins होते हैं। Cell को कैसे पता चलता है कि कौन-सा protein बनाना है? जवाब DNA की sequence में है। आइए nucleus से यात्रा शुरू करें।'),
('nucleus','Inside the nucleus','DNA is packaged with proteins',
'Nucleus में DNA, proteins के साथ chromatin बनाता है। Cell division के दौरान यही material compact chromosomes के रूप में दिखाई देता है। Chromosome हमेशा X-shaped नहीं रहता। DNA में stored information cell के कई functions को control करने में मदद करती है।'),
('dna','The double helix','Two complementary, antiparallel strands',
'DNA का पूरा नाम deoxyribonucleic acid है। इसकी दो strands twisted ladder जैसी double helix बनाती हैं। Ladder की sides sugar और phosphate से बनी हैं। बीच के rungs nitrogenous bases के pairs हैं। अलग रंग components को पहचानने के लिए दिए गए हैं।'),
('nucleotide','One nucleotide','Phosphate + Deoxyribose sugar + Base',
'DNA की basic unit nucleotide है। हर nucleotide में phosphate group, deoxyribose sugar और nitrogenous base होता है। चार मुख्य bases हैं, adenine, thymine, guanine और cytosine। इन्हें A, T, G और C लिखते हैं। इनका क्रम information बनाता है।'),
('dna','Complementary base pairing','A–T: 2 hydrogen bonds · G–C: 3',
'Adenine, thymine के साथ pair करता है, और guanine, cytosine के साथ। A और T के बीच दो hydrogen bonds होते हैं; G और C के बीच तीन। इस complementary pairing से एक strand की sequence जानकर दूसरे की sequence पता कर सकते हैं।'),
('dna','Strand direction','5′ → 3′ opposite 3′ → 5′',
'DNA strands की direction होती है। एक five prime से three prime दिशा में जाता है, जबकि दूसरा विपरीत दिशा में। इसलिए इन्हें antiparallel कहते हैं। ये नाम sugar के carbon positions से जुड़े हैं। आगे information पढ़ने की direction पर ध्यान रखिए।'),
('dna','What is a gene?','A DNA sequence that produces a functional product',
'Gene, DNA का ऐसा region है जिससे functional product बन सकता है। यह RNA हो सकता है; कई genes की information से proteins बनते हैं। हम एक protein-coding gene को follow करेंगे। DNA में regulatory और दूसरे regions भी होते हैं।'),
('central','Information flow','DNA → RNA → Protein',
'Protein-coding information आम तौर पर DNA से RNA और फिर protein तक पहुँचती है। DNA से RNA बनाना transcription है। RNA के अनुसार amino acids जोड़ना translation है। DNA खुद protein में नहीं बदलता। उसकी information नए molecules बनाने के लिए पढ़ी जाती है।'),
('transcription','Transcription begins','RNA polymerase opens a local DNA region',
'Transcription की शुरुआत में RNA polymerase और आवश्यक factors promoter region पर काम करते हैं। DNA का छोटा हिस्सा खुलता है। Polymerase एक strand को template बनाता है। पूरा chromosome नहीं खुलता, केवल संबंधित region में local opening बनती है।'),
('transcription','Making an RNA copy','Template read 3′ → 5′ · RNA made 5′ → 3′',
'Polymerase template को three prime से five prime दिशा में पढ़ता है। नया RNA five prime से three prime दिशा में बनता है। RNA में thymine की जगह uracil है। Template के A के सामने U, T के सामने A, और G के सामने C जुड़ता है।'),
('sequence','Follow one coding sequence','Coding DNA: 5′ ATG GCT TTT GAA TGA 3′',
'Coding DNA की teaching sequence देखें, ATG, GCT, TTT, GAA, TGA। RNA है, AUG, GCU, UUU, GAA, UGA। यह coding strand जैसा है, लेकिन T की जगह U है। Polymerase वास्तव में complementary template strand को पढ़ता है।'),
('rna','RNA processing in eukaryotes','5′ cap · Splicing · Poly-A tail',
'Eukaryotic cells में शुरुआती RNA process होता है। Five prime cap और poly-A tail protection और उपयोग में मदद करते हैं। Splicing में introns हटते हैं और exons जुड़ते हैं। अब mature messenger RNA, यानी mRNA, protein synthesis के लिए तैयार है।'),
('nucleus','Export through a nuclear pore','mRNA travels to the cytoplasm',
'Mature mRNA nuclear pore से cytoplasm में पहुँचता है। DNA nucleus में रहता है और RNA copy ribosome तक जाती है। सभी RNA proteins नहीं बनाते। Ribosomal RNA और transfer RNA जैसे दूसरे RNAs, protein synthesis में अलग भूमिकाएँ निभाते हैं।'),
('ribosome','The ribosome','Two subunits made of rRNA and proteins',
'Ribosome, RNA और proteins से बनी molecular machine है। इसकी small और large subunits mRNA के साथ assemble होती हैं। Ribosome sequence को तीन bases के groups में पढ़ता है। हर group codon है। सही reading frame amino acids का क्रम तय करता है।'),
('sequence','The genetic code','AUG starts · UAA, UAG and UGA stop',
'Genetic code में 64 codons हैं। Standard code में 61 amino acids specify करते हैं और तीन stop signals हैं। AUG सामान्य start codon है और methionine specify करता है। UAA, UAG और UGA stop codons हैं। अलग codons एक ही amino acid specify कर सकते हैं।'),
('trna','Transfer RNA is the adaptor','Anticodon matches codon · Amino acid at 3′ end',
'tRNA एक adaptor है। इसका anticodon, mRNA के complementary codon से pair करता है। दूसरे सिरे पर specific amino acid जुड़ा होता है। Enzymes सही amino acid को सही tRNA से जोड़ते हैं। इस तरह nucleotide sequence का संबंध amino acid sequence से बनता है।'),
('ribosome','Translation begins','Initiator tRNA recognizes the start codon',
'Translation शुरू होते समय ribosome start codon पर reading frame स्थापित करता है। Initiator tRNA, methionine लाता है। अगला codon अगले amino acid का चयन कराता है। ध्यान दें, ribosome DNA को सीधे नहीं पढ़ता। यहाँ template mRNA है।'),
('ribosome','Building the chain','Peptide bonds join amino acids',
'Ribosome में amino acids के बीच peptide bond बनता है। Growing chain एक tRNA से दूसरे पर transfer होती है। Ribosome आगे बढ़ता है, खाली tRNA निकलता है और नया tRNA आता है। इस दोहराए जाने वाले process को elongation कहते हैं।'),
('sequence','Decode our example','AUG GCU UUU GAA UGA → Met–Ala–Phe–Glu–Stop',
'हमारी sequence में AUG से methionine, GCU से alanine, UUU से phenylalanine और GAA से glutamate जुड़ता है। अगला UGA stop signal है। यह छोटी teaching sequence है। वास्तविक proteins में अक्सर सैकड़ों amino acids विशेष क्रम में जुड़े होते हैं।'),
('ribosome','Termination','A release factor recognizes the stop codon',
'Stop codon आने पर सामान्य amino-acid-carrying tRNA की जगह release factor काम करता है। Polypeptide chain release होती है और translation समाप्त होती है। Ribosome की subunits और दूसरे components अगली protein synthesis में फिर इस्तेमाल हो सकते हैं।'),
('protein','From a chain to a protein','Sequence guides folding and function',
'Polypeptide, amino acids के interactions से खास three-dimensional shape में fold होता है। कुछ proteins को folding helpers, chemical modifications या दूसरी chains से जुड़ने की ज़रूरत होती है। Shape उसके काम के लिए महत्वपूर्ण है, जैसे enzyme का active site।'),
('mutation','When the sequence changes','A mutation may alter a protein—or have no effect',
'DNA sequence में बदलाव mutation है। इससे amino acid बदल सकता है, stop signal बन सकता है, या protein sequence अपरिवर्तित रह सकती है। एक base का insertion या deletion reading frame बदल सकता है। हर mutation harmful नहीं होती; असर बदलाव और उसके स्थान पर निर्भर है।'),
('central','Gene regulation','Different cells use different sets of genes',
'बहुत-सी body cells में लगभग वही DNA है, फिर भी nerve और muscle cells अलग काम करती हैं। उनमें अलग genes सक्रिय होते हैं। Cell regulate करती है कि कब, कहाँ और कितना RNA या protein बने। Information का उपयोग नियंत्रित होता है।'),
('central','From gene to protein','Transcription copies information · Translation reads the code',
'कहानी दोहराएँ। Gene से transcription द्वारा RNA बनता है। Eukaryotic mRNA process होकर cytoplasm में जाता है। Ribosome codons पढ़ता है, tRNA amino acids लाता है और peptide bonds से chain बनती है। यह fold होकर functional protein बन सकती है। Sequence से structure और structure से function।')]

# Reference-aligned editorial cues. Camera movements are procedural reconstructions.
CELL = [
(0,'cell','The Fundamental Unit of Life','Complete Chapter'),(19.2,'cell','Cells','The basic unit of life'),
(23.12,'cork','Cells','Robert Hooke · Cork'),(29,'cork_micro','Cork under a microscope','A honeycomb of cell walls'),(37.44,'microscope','Cells','Robert Hooke · 1665'),(44,'cork_micro','Cells','Cell = a small compartment'),
(60.72,'onion','Observing onion cells','Prepare a temporary mount'),(70,'onion_peel','Onion epidermis','A thin peel'),(77.12,'slide','Watch glass','Keep the peel in water'),(92.8,'slide','Glass slide','Add water'),(98.72,'slide','Transfer the peel','Keep it flat'),(109.68,'stain','Safranin solution','Stain the specimen'),(119.28,'slide','Cover slip','Lower gently · Avoid air bubbles'),(126.56,'microscope','Compound microscope','Observe the temporary mount'),(136,'onion_cells','Onion epidermal cells','Basic building units'),(149.44,'onion_cells','Cells','Organisms are made of cells'),
(156.96,'cell','2. Cell Structure','Cell structure and its components'),(162.56,'microscope','Cell structure and its components','Observing cells'),(175,'cell','Cell structure and its components','Plasma membrane · Nucleus · Cytoplasm'),(187.52,'cell','Cell structure and its components','Coordinated cellular activities'),
(201.52,'cell','Plasma membrane or cell membrane','The cell boundary'),(216.72,'membrane','Selectively permeable membrane','Regulated transport'),(231.36,'membrane','Selectively permeable membrane','Some substances cross more readily than others'),(241.04,'diffusion','Diffusion','O₂ and CO₂ move down their gradients'),(253.84,'osmosis','Osmosis','Net movement of water across a selectively permeable membrane'),(269.76,'osmosis','Osmosis','Net water flow: dilute solution → concentrated solution'),(283.28,'cell','Flexible plasma membrane','Organic molecules'),(289.12,'bilayer','Lipids and proteins','Phospholipid bilayer with embedded proteins'),(295.6,'microscope','Electron microscopy','Reveals cellular ultrastructure'),
(303.2,'cell_full','3. Cell Organelles','Specialized structures within a cell'),(309.52,'cell_full','Cell organelles','Different structures · Different functions'),(334.8,'cell_full','Cell organelles','Coordinated activities'),(359.2,'er','Endoplasmic reticulum','Membrane-bound tubes and sheets'),(370.24,'golgi','Golgi apparatus','Stacked cisternae'),(375.76,'lysosome','Lysosomes','Digestion and recycling'),(381.76,'mitochondria','Mitochondria','ATP production'),(389.04,'chloroplast','Plastids','Found in plants and algae'),(394.8,'cell_full','Cell organelles','Working together'),
(407.92,'er','1. Endoplasmic reticulum','A network of membranes'),(432.24,'er','Two types of ER','Rough ER · Smooth ER'),(446.64,'er','Ribosomes','Attached ribosomes give RER a rough appearance'),(456,'er','Proteins and lipids','Correction: ribosomes/RER make proteins; SER makes lipids'),(468.88,'bilayer','Membrane biogenesis','Proteins and lipids build cellular membranes'),
(480.24,'golgi','2. Golgi Apparatus','Camillo Golgi'),(488,'golgi','Cisternae','Parallel stacks of flattened membrane sacs'),(500,'golgi','The endomembrane system','ER–Golgi transport occurs in vesicles'),(513.52,'golgi','Vesicular transport','Cargo moves through the Golgi'),(525.84,'golgi','Functions','Storage · Modification · Packaging'),(539.2,'golgi','Lysosome formation','Golgi sorts digestive enzymes'),
(546.88,'lysosome','3. Lysosomes','Membrane-bound sacs with digestive enzymes'),(555.6,'lysosome','Digestive enzymes','Synthesized by ribosomes on rough ER'),(562,'lysosome','Cellular recycling','Digest worn-out components and foreign material'),(575,'lysosome','Digestion','Complex material → reusable building blocks'),
(590.08,'mitochondria','4. Mitochondria','Powerhouse of the cell'),(598.48,'mitochondria','Two membranes','Outer membrane · Inner membrane'),(605.04,'mitochondria','Cristae','Inner membrane folds increase surface area'),(612.24,'mitochondria','ATP production','Adenosine triphosphate'),(621.36,'mitochondria','ATP','Transfers usable chemical energy'),(633.68,'mitochondria','Energy currency of the cell','Energy for cellular work'),(646.4,'mitochondria','Mitochondrial DNA and ribosomes','Mitochondria synthesize some of their own proteins'),
(663.68,'plastids','5. Plastids','Plastids occur in plants and algae'),(671.04,'plastids','Types of plastids','Chloroplasts · Chromoplasts · Leucoplasts'),(676.56,'chloroplast','Chloroplasts','Chlorophyll · Photosynthesis'),(688.48,'chloroplast','Photosynthetic pigments','Chlorophylls and accessory pigments'),(699.76,'leucoplast','Leucoplasts','Storage: starch, oils or proteins'),
(707,'nucleus','4. Nucleus and Cytoplasm','Genetic information and the cellular interior'),(714.24,'nucleus','Nucleus','A double-membrane organelle'),(724.64,'cell','Eukaryotic cells','A membrane-bound nucleus'),(733.6,'comparison','Prokaryotes and eukaryotes','Prokaryote: nucleoid · Eukaryote: nucleus'),(750,'nucleus','Nuclear envelope','Two membranes'),(755.2,'nucleus','Nuclear pores','Regulated exchange with the cytoplasm'),(764.4,'nucleus','Nuclear transport','Proteins and RNA cross through nuclear pores'),(771.28,'chromosome','Chromosomes','DNA packaged with proteins'),(780.48,'dna','DNA','Hereditary information'),(793.28,'division','Cell division','Genetic information passes to daughter cells'),(805.6,'cell','Cellular control','Gene expression guides cellular activities'),(819.04,'bacteria','Bacteria','No membrane-bound nucleus'),(831.44,'bacteria','Nucleoid','DNA-containing region without a nuclear envelope'),(841.84,'cell','Cytoplasm','Region inside the plasma membrane, outside the nucleus'),(853.52,'cell','Cytoplasm','Correction: cytoplasm is a cell region, not a membrane'),(861.36,'cell','Cytosol and organelles','Cytosol is the fluid component'),(869.68,'cell_full','Specialized cell organelles','Each structure performs particular functions'),(881.52,'outro','Visual Learning','Learn visually. Understand deeply.')]

def main():
    manifests={}
    for name, rows in [('heart',HEART),('dna',DNA)]:
        shots=[]
        for i,(asset,title,subtitle,narration) in enumerate(rows):
            shots.append(dict(id=f'{name}_{i:03d}',index=i,asset=asset,title=title,subtitle=subtitle,narration=narration,start=i*20.,duration=20.,frames=480,chapter=name,variant=i))
        manifests[name]=dict(id=name,title=rows[0][1],fps=24,width=1920,height=1080,target_duration=480,shots=shots)
        (ROOT/'scripts'/f'{name}.hi.md').write_text('# '+rows[0][1]+' — Hindi narration\n\n'+'\n\n'.join(f'## {i+1:02d}. {r[1]}\n\n{r[3]}' for i,r in enumerate(rows)))
    shots=[]
    for i,(start,asset,title,subtitle) in enumerate(CELL):
        end=CELL[i+1][0] if i+1<len(CELL) else 891.0833333333334
        sf=round(start*24);ef=round(end*24)
        shots.append(dict(id=f'cell_{i:03d}',index=i,asset=asset,title=title,subtitle=subtitle,start=sf/24,duration=(ef-sf)/24,frames=ef-sf,chapter='cell',variant=i))
    manifests['cell']=dict(id='cell',title='The Fundamental Unit of Life',fps=24,width=1920,height=1080,target_duration=891.0833333333334,shots=shots)
    for name,m in manifests.items():
        (ROOT/'storyboards'/f'{name}.json').write_text(json.dumps(m,indent=2,ensure_ascii=False))
    print({k:len(v['shots']) for k,v in manifests.items()})

if __name__=='__main__':main()

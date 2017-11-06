[33mcommit db72e78da1b8f1ed08893b81c65038e843414a1d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Nov 6 11:51:21 2017 -0600

    Refactoring for production run

[33mcommit b65e3cfec6e2239796ff7b6139bd1ba4985053b9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Nov 6 11:32:26 2017 -0600

    Refactoring for production runs.

[33mcommit 864e12d175ba791dc8f924c709ec677c36ca6d3f[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 31 20:41:05 2017 -0500

    Rebuild model on QC failure

[33mcommit d8bc5567d71f305daa4ce26327845e79dbc522ca[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 31 20:25:21 2017 -0500

    KeyError bug fix

[33mcommit f6a30053e56c2ea1683f4205a6baae3509541678[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 31 19:45:26 2017 -0500

    Logging improvements.

[33mcommit 4baaaccb6956c8fbb86078b67c215c612fa22cd3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 31 17:55:12 2017 -0500

    Allow QC to focus on potential outliers.

[33mcommit 2838d599ba589352c5d55d43ee1a2d17a0de5ad6[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Oct 30 23:01:51 2017 -0500

    Cap growth of semantically duplicate records in the labeled dataset to N to prevent training bias.

[33mcommit f0c221b4eecfda2280bceb451a7a8b03ad2b1193[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 18:17:16 2017 -0500

    Classify input files using four different models

[33mcommit e951cbc4fc56f2ac6bfa23bc7532bd2c7b20efb1[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 17:56:34 2017 -0500

    Corrected model archive name to match the model name.

[33mcommit 861e9626231ceb7625859367b4e803620b612a76[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 17:41:56 2017 -0500

    Fix model archive name discrepancy

[33mcommit 1cb50be29782213c610ec7ae467707032d5c9523[m
Merge: 315030d 2f5e6af
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 17:37:52 2017 -0500

    Merge branch 'master' of https://github.com/dkhanal/maude_experiments

[33mcommit 315030d24adfdba06fa6a0b9f852e8f796e65554[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 17:37:39 2017 -0500

    Configuration adjustment

[33mcommit 2f5e6affabdfa8d5fe5ece6174f5c04d65f868c0[m
Merge: abe8551 defc5b4
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 20:05:00 2017 +0000

    Merge branch 'master' of http://github.com/dkhanal/maude_experiments

[33mcommit abe8551e1a93cb282af16064f7217d55000ca9c3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 20:04:35 2017 +0000

    Switch model to use non-duplicate records to remove bias.

[33mcommit defc5b43613f3b999a7445860a775e756b8a41eb[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 15:01:00 2017 -0500

    Allow QC on the entire auto-labeled set.

[33mcommit a9d024d298f73a16771a70c8a18cd2ad0d25efae[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 12:29:20 2017 -0500

    Allow autolabeled data to be input into modeling

[33mcommit edfb43fa95f2d357a896198fb2df37baee396992[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 12:15:33 2017 -0500

    Create directory for input datasets at startup

[33mcommit 13d9508e760929b191ae3b0c041e4beed759d93e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 10:40:58 2017 -0500

    Corrected typo in remote file name.

[33mcommit 2f6eeacc010918de2383bb90ab1fd85d2c18607d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 10:31:18 2017 -0500

    Added pre-labeled datasets to the collection

[33mcommit 28fdfd644d810ef7f638bf8e37df230557bdec5f[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 29 09:29:58 2017 -0500

    Added auto-labeled directory to configuration

[33mcommit 4437e2b6838434680ceb1132e4393b2af05012f8[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 16:23:15 2017 -0500

    Source auto-labeling input from pre-labeled datasets

[33mcommit a03f8fe425d1ac067d1c4477f771014733df8490[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 16:08:08 2017 -0500

    Cleanup of unused file references

[33mcommit a57c8fe1f8a50cb199cb43992589b521d21e6884[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 16:06:19 2017 -0500

    Cleanup of unused file references

[33mcommit 16e7eb0b0710e06bb34d71bb7759828d49afaa54[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 16:03:14 2017 -0500

    Fixed list of files to upload

[33mcommit 9110b6b29cc6d0760dfe0a024a88033002173211[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 16:01:35 2017 -0500

    Corrected file names to upload

[33mcommit e1710760a9d2b0113a38b18771aa7e0efa78c972[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 15:57:27 2017 -0500

    Corrected remote blob names

[33mcommit 82a41a0a9165fb964bf0390d7d2b3498fcd5649f[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 15:43:48 2017 -0500

    Remote blob name correction

[33mcommit 1ab69b97941466c287761f06aedf7a0fde53c044[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 28 15:27:15 2017 -0500

    Support auto labeling

[33mcommit 269210cd00d480da3e2e98a4b2e5a1e3067ce96d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 24 14:21:34 2017 -0500

    Reset target dataset size to the entire available set.

[33mcommit 0119d5c8bdbe16ea45f7753e396b4c8200116069[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Oct 23 13:05:47 2017 -0500

    Format summary output for import/analysis

[33mcommit 1d8e6a294a1f344645df4d9e525b7b0c60e5f8f9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Oct 23 10:07:19 2017 -0500

    Reset the classification threshold. Set the target record size to 100k per file (for experimental run).

[33mcommit b7d610c39971937b91bf1efbaca0b47972e66f69[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 22 15:05:54 2017 -0500

    Increase positive classification threshold to .65

[33mcommit 2555348115bed0df1081371f07f752c5af3adb67[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Oct 21 11:30:24 2017 -0500

    Configure classification input data sets.

[33mcommit 463c0b1cd97cb82e7d5a17e69d2414e09accebf1[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Oct 16 21:36:58 2017 -0500

    Always download models to be used in classification.

[33mcommit d0acff2997aa1989b019fa5a6b396ebed3b660f9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 15 18:23:58 2017 -0500

    Remove entirely identical records from labeled datasets.

[33mcommit 3fd9381d2e2a80dc5c03dd9ba08a53a7d4d10cc2[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 15 18:21:10 2017 -0500

    Remove entirely identical records from labeled datasets.

[33mcommit 6ca01d770481b84b3a4107c715859ea9137b21cf[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 15 11:57:10 2017 -0500

    Always download models

[33mcommit 898054baf063f8a1d448835db76cd0ccfb9fb122[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 15 11:51:37 2017 -0500

    Randomize labeled data set before models are trained on it.

[33mcommit eb820afe8023fcaed97324460aaec46bb773d6c3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 10 20:55:18 2017 -0500

    Show labeling accuracy over last 500 prompts

[33mcommit 2da7f45488effe7058864ed26272a1fa5b87ccbe[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Oct 10 14:49:28 2017 -0500

    Log/report accuracy scores on sklearn models.

[33mcommit f8c860536bede3bbf6cf3b41774260edcc9a9158[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 8 18:14:57 2017 -0500

    Enable targeted sourcing of pre-labeled data to allow parity between positive and negative records.

[33mcommit f035083bfc538d074696a8f7d10ab7e8013eb806[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 8 18:06:36 2017 -0500

    Enable targeted sourcing of pre-labeled data to allow parity between positive and negative records.

[33mcommit 6059e46fbdbbfaff1d4ba3bec7e97652cdbf959e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 8 15:16:05 2017 -0500

    Fixed tuple unpacking issue.

[33mcommit 92c7a6bdb2eda1b24cd5cc586475e8b4046a357b[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Oct 8 13:37:30 2017 -0500

    Support classification summary for all configured models.

[33mcommit eb44c568c4630404cf1c0460b031c82742a402d8[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 11:01:42 2017 -0500

    Only allow input in supported range.

[33mcommit 436977299593e4e8bdac780bf25b2ae9e13a0e78[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 10:58:21 2017 -0500

    Only allow input in supported range.

[33mcommit 6a86da1bf68262bac478e8b58c4b822eebccefd2[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 10:53:58 2017 -0500

    Only allow input in supported range.

[33mcommit 7427da06e1b308803c03f3318635daf4061845e7[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 10:16:47 2017 -0500

    Added labeling accuracy for overall decision support.

[33mcommit 18355775caad49abcc59c287ca3fcd1d6e26de90[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 10:12:25 2017 -0500

    Added labeling accuracy for overall decision support.

[33mcommit 45a3f91a6825cc61bd02a9db23a11255bfac343d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 21 09:59:56 2017 -0500

    Added labeling accuracy for overall decision support.

[33mcommit bbb6f876ce03e2bd61b603fe5d49e76279e7a717[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Sep 20 22:19:01 2017 -0500

    Imported nltk.

[33mcommit 40bb2da24634d526768e2a36e7cd36686ecf3a2c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Sep 20 22:07:02 2017 -0500

    Removed unnecessary output line.

[33mcommit 43fe3d8061f20cc528410096886d4a3183e94bae[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Sep 20 21:39:15 2017 -0500

    Bug fix and documentation.

[33mcommit fce82c801e8aae1fc5d9c32b52d0785a4e138a81[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Sep 19 07:56:16 2017 -0500

    Support persistence of labeling accuracy metrics.

[33mcommit 41f7568bfaa5e9d272075902577be7536e59b8fb[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Sep 19 00:07:53 2017 -0500

    Labeling prediction accuracy computation for each model.

[33mcommit 8c529f4253e45f87eefcc7ba0bcc197dd39e885f[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Sep 16 00:21:50 2017 -0500

    Integration of SGD and voting classifiers in labeling decision support.

[33mcommit be7b7f799d107d19267ece4829ebd780978b592d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Sep 14 00:20:11 2017 -0500

    Initial integration of sklearn models.

[33mcommit 25a5cf17e63ebe498bc30153cbef4b1adc6b61e4[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Sep 12 00:06:58 2017 -0500

    Refactoring to support SVM models.

[33mcommit 7775675d1e77b6d06cea2db747705620cc0ab5f2[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Sep 9 17:24:17 2017 -0500

    Bug fixes.

[33mcommit 6c4d58e2d735e569a605c4df1a2a5cea7a760e37[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Sep 3 12:25:39 2017 -0500

    Support upload of log files.

[33mcommit 016f94cb6729b21dd7d5121860d0b0524ba27e47[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Sep 2 15:28:23 2017 -0500

    Integrated upload into main -- with an argument.

[33mcommit 7d2c283b4337d77bfc5107e6a514ff8cdf4fad78[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Sep 2 14:02:48 2017 -0500

    Added output uploader.

[33mcommit 1014f84bc627f2b7db256baf7cb05150ed033518[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 19:59:47 2017 -0500

    Set max record to extract to a very high value.

[33mcommit 01c4f308729abcbc94faa346c3091c55e38efc55[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 19:56:46 2017 -0500

    Config bug fix.

[33mcommit 0d6448369db1a2914a08e549f334f61921515a67[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 19:42:33 2017 -0500

    Configuration adjustments.

[33mcommit de65bb1afb7bd52afc52bbd6da2adb28e1037160[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 19:31:48 2017 -0500

    Configuration update.

[33mcommit ccad673ceda4467001d1c0884b6dc5dc298e5bb2[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 19:29:28 2017 -0500

    Refactoring to support local filesystem as 'remote server', in addition to the Azure cloud.

[33mcommit 8cab7283bbd25de9c0482088f97477e8bd73c97e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 18:08:11 2017 -0500

    Refactoring

[33mcommit e69a2fe73cb3cb1be1042d696d2aca1229a0aa25[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 10:55:03 2017 -0500

    Refactoring.

[33mcommit e3ff493872c9b1e5c88ef6bad5d10c27d2405835[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Sep 1 09:21:35 2017 -0500

    Added helper files.

[33mcommit d29bf1332157a6954e59daad2235e565ce8aa1da[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 31 22:30:24 2017 -0500

    Bug fix.

[33mcommit f83b27efc6e76408017b6d6bc4eba08d7d359eee[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 31 22:27:40 2017 -0500

    Extracted common code to shared library. Switched from print to logging, various other improvements.

[33mcommit 916de1c42ffde3b5a2bf125c129512c221eb2da9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 29 18:18:06 2017 -0500

    Additional labeling improvements.

[33mcommit a4df24ba4d1b06369d17611c74017b9efdae7107[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 29 18:13:49 2017 -0500

    Support for trigrams, additional labeling improvements.

[33mcommit 2a1493a3f022850d0a37f47157f756170092f8f3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 29 18:12:55 2017 -0500

    Support for trigrams, additional labeling improvements.

[33mcommit f960d49e88dbe8dbaeb378d6d6af66f259bc9237[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 27 18:42:50 2017 -0500

    Accounted for the scenario where no model exists yet to provide a labeling suggestion.

[33mcommit 0822cfee40d3eeed0c407eedd2ca91000b301c70[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 27 18:33:50 2017 -0500

    Configuration update.

[33mcommit d034808be1688e865b86513de0d20f2d2e0ce42e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 27 18:30:34 2017 -0500

    Fix a zero negative featuresets bug

[33mcommit 31eb1691e82b23ef11e45bfe16f17f618e2e9945[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 27 13:53:39 2017 -0500

    Added bigram models.

[33mcommit eb841147235ca77a3ba315b4dec92b072342812c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 26 23:13:39 2017 -0500

    Minor message update.

[33mcommit 883ba3f9835d3c1989407511c9262912328f07e5[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 26 09:44:12 2017 +0000

    Fixed tuple list append bug

[33mcommit 1a0315db47eae2e386511fbb0167118dcfefa348[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 26 09:19:03 2017 +0000

    Fixed cross platform path issue

[33mcommit 994fb675b0f6451a795b12f43b8c50eb49be6cc9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 17:11:30 2017 -0500

    Continuous feedback loop loop implementation - integration of classification feedback into labeling.

[33mcommit 383465d64d6c39fb00d62c5d74f66392f696f628[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 17:10:26 2017 -0500

    Continuous feedback loop loop implementation - integration of classification feedback into labeling.

[33mcommit dc682cde508498dcdae20fead2d9ad740160a966[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 15:47:39 2017 -0500

    Continious feedback loop loop implementation - Automatic model regeneration.

[33mcommit d728cb807afa2946c9d1c731ab1f0a436c6b5ba1[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 15:30:21 2017 -0500

    Continious feedback loop loop implementation - Model regeneration integration.

[33mcommit 0f0d2406b6bfc9799890bcb34c9fa1e514ce4d58[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 14:27:13 2017 -0500

    Refactoring of model generation.

[33mcommit 9448bb44a81690c56dd3fb0dfb82e4cab36abf7c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 12:33:27 2017 -0500

    Configuration and message adjustments.

[33mcommit 7cd607753628e6fbcb4019705bc4fd052bd08fd0[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:44:06 2017 -0500

    Display improvement.

[33mcommit 71d9eefd6d0276fa6e94e53b5174a112ec9afccc[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:38:39 2017 -0500

    Append labeled records.

[33mcommit 09a32bbced54059f7311da0db53b251c5829d887[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:29:44 2017 -0500

    Display current totals..

[33mcommit 9f9d10cc699fa1124993f70ba62470e740300fa9[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:20:11 2017 -0500

    Bug fix.

[33mcommit 04662b45352f963e7f825387125fc3ea438d46dd[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:14:54 2017 -0500

    Create input/output directories during setup.

[33mcommit ccba42372979399d819f5c6da2261d58dcf2a736[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 25 00:06:20 2017 -0500

    Random selection of candidate record for labeling verification.

[33mcommit d8fcb21d786a0fca2e1782a3dd4ae729aea99ef8[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 18:38:08 2017 -0500

    Ability to upload manually verified records

[33mcommit 484fa09a1d6f7c5bb61cd365d5a9d7b313ee9d5d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 16:43:34 2017 -0500

    Add a new line to the pos/neg last record number data.

[33mcommit 06ad71d0f2a9b748f87b571623a23d05888a2e00[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 16:39:46 2017 -0500

    Preserve last read record number for both positive and negative labeled sets.

[33mcommit 9ed078493af62ac17fd822d9d2676e2529c88999[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 16:13:18 2017 -0500

    Linux adjustments

[33mcommit 8c8af369a9b17b778d054a1c42afa656e7599be0[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 16:10:22 2017 -0500

    Adjustment for linux

[33mcommit bdf108e3d878dc3ff77db8e86104bc91ac2241f7[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 15:04:45 2017 -0500

    Config adjustment.

[33mcommit 9b526d4d7b1f19ac1b80699ac7e60407bad6ef80[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 14:01:07 2017 -0500

    Set input file encoding.

[33mcommit f342f17d03749d76b56215141e14e5874a101c6e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 13:37:10 2017 -0500

    Cleanup

[33mcommit efac5e34cea70ca5521d853111ad501d696a0bd4[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 13:30:45 2017 -0500

    Cleanup of old files during initialization.

[33mcommit 5b13134a9b57b5fc4b9a82ff03452b2c80b11806[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 11:56:20 2017 -0500

    Classification improvement.

[33mcommit 731dba29a80fca45edc927d50f28099951684ece[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 11:15:54 2017 -0500

    Support elimination of duplicate labeled records in model generation.

[33mcommit 797ec2525961ba4376812d45ec2af41d50b63d45[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 12 02:02:53 2017 -0500

    Labeled records verifier implementation.

[33mcommit 926b3983f6f75aee070c3e57a3a02028c5db7d10[m
Merge: cda9d4f 8b1fb87
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 10 09:41:04 2017 -0500

    Configuration adjustment

[33mcommit cda9d4f592e748ec2d6f78476be311cdaf4a6b0b[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 10 09:35:58 2017 -0500

    Wrote a tool to perform manual labeling of records.

[33mcommit 8b1fb87a6a9b34e1102b1e51ec97a3dee56671f9[m
Merge: d45d823 758a3cc
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 10 08:36:31 2017 -0500

    Merge remote-tracking branch 'origin/master'

[33mcommit d45d823082b8dc29054d302c2f7f2d33985bd74d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Aug 10 08:33:14 2017 -0500

    Configuration adjustment.

[33mcommit 758a3cc46349fdc8b3eb0391697462b863f3c9f6[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Aug 9 22:55:32 2017 -0500

    Wrote a tool to perform manual labeling of records.

[33mcommit 55d9b82c019cf031bf26fe2ea40b074e20ced739[m
Merge: 1a95b70 ac3d4a6
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 8 19:25:59 2017 -0500

    Merge remote-tracking branch 'origin/master'

[33mcommit 1a95b70318d5b7c9f57aa1b71129a494b244c918[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 8 19:25:40 2017 -0500

    Dump of all first-pass labeled records.

[33mcommit ac3d4a6679ff240ecb94722fb4e698462c735aeb[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Aug 8 14:01:36 2017 -0500

    Upload labeling output to cloud.

[33mcommit 64bb3202f9da81edbd02c84e0f60004cb72193ad[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Aug 7 12:53:46 2017 -0500

    Fixed import.

[33mcommit 595809e59168b2fa1cab9f0d465f9a68f858650d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Aug 7 12:52:27 2017 -0500

    Change function xrange to range.

[33mcommit 317b27fbce6092cb0cb15ccf30d14240a81a0475[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 23:40:16 2017 -0500

    Match the number of positive and negative labeled records during extraction.

[33mcommit 905d4f48c0fbabdfe760bf958a2642f039ba41c4[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 18:57:04 2017 -0500

    Optimization of labeling parameters.

[33mcommit cb17cef7799452436bb60c373628151a1eb1893e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 18:11:46 2017 -0500

    Optimization labeling parameters.

[33mcommit 36b669b5a84236d178c42bce9046a2bff3e7ba31[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 15:27:17 2017 -0500

    Expanded classification to entire input dataset.

[33mcommit a03a43dbe8919ffd74158a779d2eb666a7954a8c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 15:03:30 2017 -0500

    Limit the number of negative labeled records to the number of positive labeled records.

[33mcommit 88da3d8266c0119079e70001797da534dde9e83d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 14:04:53 2017 -0500

    Modeling improvements.

[33mcommit 0079abf8c16a8d8388750651c27edb650cea5534[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Aug 6 13:10:55 2017 -0500

    Added a missing configuration parameter.

[33mcommit 60d319921dad6cc9cff1215a574671940da66181[m
Merge: 9818cd2 03f174b
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 17:42:12 2017 -0500

    Sync with remote.

[33mcommit 9818cd24a3a1b61f755bcafb48d9e614a24355bf[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 17:37:11 2017 -0500

    Config adjustment.

[33mcommit 03f174b529eb1bf5c59f35fec2487f59b5a347a1[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 16:27:34 2017 -0500

    Configuration adjustment.

[33mcommit 5577eab1c3b3bd29bb678ed2e16deae0f87824c5[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 09:14:20 2017 -0500

    Allow larger chunks of files to reduce context switching on parallelization.

[33mcommit 00d3788c63b19d4c70a1026b51d84356543dd071[m
Merge: 051722d cc18d1d
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 08:57:45 2017 -0500

    Merge branch 'master' of https://github.com/dkhanal/maude_experiments

[33mcommit 051722d7ecaefe56a3141e740530e12003520be4[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Aug 5 08:57:39 2017 -0500

    Config changes.

[33mcommit cc18d1d8990263fe055a9ed9aac2a28415ee04f3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Aug 4 22:52:12 2017 -0500

    Pre-compile regex patterns for performance.

[33mcommit a7e21628631b0a3589e5746c532ea300f17e91fc[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Aug 2 14:51:33 2017 -0500

    Configuration adjustment.

[33mcommit bbedb0b1f042cab4d20c6008f410fc47ede92cf2[m
Merge: 80a079c f41caea
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 30 17:19:58 2017 -0500

    Merge branch 'master' of https://github.com/dkhanal/maude_analysis

[33mcommit 80a079ca9a5d81ffd4f8f76e848b721373ca3b85[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 30 17:18:16 2017 -0500

    Config update.

[33mcommit f41caeab62f07e71bada6ab83807245656b29da5[m
Author: dkhanal <dkhanal@gmail.com>
Date:   Sun Jul 30 17:12:47 2017 -0500

    Update README.md

[33mcommit be723ef503ea074225ca21df6135b6ecf37f4198[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Jul 26 15:54:00 2017 -0500

    A massive parallelization of the labeling work.

[33mcommit 9aae719f9a07be4efe79ed44dd5c1b1ad319ef52[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Jul 26 14:26:11 2017 -0500

    Changed default file split size.

[33mcommit cef76e62963b4613af87884e77f53c604bc9b69d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Tue Jul 25 08:32:33 2017 -0500

    Added multiprocessing capability.

[33mcommit 79846407c445f1c299ea482d8eff0c9c336da646[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Jul 24 21:42:47 2017 -0500

    Split input files into chunks for parallel processing.

[33mcommit bee9a449c71b2bbb1dd712b489ad00ae3ae64c98[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Mon Jul 24 18:17:18 2017 -0500

    Various improvements

[33mcommit 72652d60df4122973771874e836cab5ce90c5e0e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 14:32:15 2017 -0500

    Documentation

[33mcommit d4cb680fb6c66b6c127010d4507294a2a921042e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 14:22:43 2017 -0500

    Various improvements

[33mcommit 5b10016332eef5eceaf37233aae247f7e4532b19[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 14:11:17 2017 -0500

    Documentation

[33mcommit e75596e636773a396b09eb196acfa0af9157e8bb[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 13:27:06 2017 -0500

    Functional classifier. Additional refactoring.

[33mcommit 963cb5841c54dc7139b4ef5454d53f955035e113[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 11:07:31 2017 -0500

    Production configuration.

[33mcommit b10e387ed71910c03ca40dbd91a4ee78a531b36d[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sun Jul 23 11:00:36 2017 -0500

    Various improvements.

[33mcommit fcd6fba746b8bb1bcc58e102efbfd15ffec0223f[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 22 18:12:44 2017 -0500

    Refactored model generation portion out of classification. Redesign for distributed computing.

[33mcommit 190ea06d715d57fdcca70bf81af9f6dfafcb196e[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 22 15:02:04 2017 -0500

    Set max number of records to extract as positive or negative.

[33mcommit f4beebf424eff648e54c7d95d602d25acec3a229[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 22 14:26:22 2017 -0500

    Config fix.

[33mcommit 62d00404feced2606b20d56f494d2c7e6f413e80[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 22 14:15:35 2017 -0500

    Bug fix + restored config.

[33mcommit 2d28d5f10eff5b7d13395a44dfb6cf28ef249fd6[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 22 14:04:11 2017 -0500

    Upload output of Labeling to Cloud

[33mcommit 7bca468f465664b2aec6518b4ca3362a295b51b3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Jul 21 22:14:29 2017 -0500

    Added new patterns for labeling query

[33mcommit 59e417d7d0558329142c733436b6d5866fba006c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 20 23:23:05 2017 -0500

    Encoding fix.

[33mcommit ee718223e8acf92a3570b6de1b842087fbbbcc80[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 20 22:43:59 2017 -0500

    Allow all records in a file to be examined for extraction.

[33mcommit 3fb8a9315ab47c4b005b753031836d29910e4765[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 20 22:34:50 2017 -0500

    Remove limit from max records to label.

[33mcommit cbe4e220f20a54813bfe6b2e42872ca8b7d78b47[m
Merge: 6601079 1e51b74
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 20 22:33:05 2017 -0500

    Merge branch 'master' of https://github.com/dkhanal/maude_sw_causes

[33mcommit 660107968617fe672122bca20fe557aec3def33c[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 20 22:31:21 2017 -0500

    Allow labeling by year. Year specified as a command line argument.

[33mcommit 1e51b74b502d41ff0326c8304493cc3306f1b575[m
Author: dkhanal <dkhanal@gmail.com>
Date:   Thu Jul 20 19:26:55 2017 -0500

    Markdown syntax

[33mcommit 0ada2057605662ece4bce6394c8de9cf5ad59009[m
Author: dkhanal <dkhanal@gmail.com>
Date:   Thu Jul 20 19:22:59 2017 -0500

    Updated documentation

[33mcommit 0f46cbb38ba4667fc8c90219508faea0e278bf40[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Jul 19 22:48:56 2017 -0500

    Various improvements, refactoring and restructuring to contain memory growth.

[33mcommit c722075a4a06e2fd19e90ac4b143d523b074bb28[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Sat Jul 15 16:38:00 2017 -0500

    Various improvements.

[33mcommit e679edf9d5d658f43be01bfc95efbef92cf28466[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Jul 14 21:33:11 2017 -0500

    Various improvements.

[33mcommit 122e5776828fffcba9f28532e7dc2f8cc95d52db[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Jul 14 19:40:41 2017 -0500

    Minor doc correction.

[33mcommit 36bfd2d1f5852c6483e12b479f948aa167c114b5[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Fri Jul 14 19:39:33 2017 -0500

    Added support for pickling models and stemming.

[33mcommit 4beb96560849c68ac3853d82e132a6e3e0d069bc[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 13 22:44:07 2017 -0500

    Various improvements

[33mcommit 3c6c9086a3a1106bf1fc8f3691e77885fec043dd[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 13 22:27:04 2017 -0500

    Various improvements.

[33mcommit 5a8aaa5944067acddfaed3f4fbf05654a6170516[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Thu Jul 13 17:54:40 2017 -0500

    Various improvements

[33mcommit 0199c0a0a367e9563adaefb758d545eedf9c03ad[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Jul 12 19:34:38 2017 -0500

    Various improvements.

[33mcommit 10b3d8c01d70e170048735e159ef2592466d7bf3[m
Author: Deepak Khanal <dkhanal@gmail.com>
Date:   Wed Jul 12 18:44:42 2017 -0500

    Various improvements

[33mcommit d4479065f63a42be2577a6c6d2d656fa8eb35576[m
Author: dkhanal <dkhanal@gmail.com>
Date:   Sat Jun 24 15:21:26 2017 -0500

    Initial commit

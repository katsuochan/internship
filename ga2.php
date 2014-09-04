<?php
  require_once ("google-api-php-client/src/Google_Client.php");
  require_once ("google-api-php-client/src/contrib/Google_AnalyticsService.php");

 session_start();
 $client = new Google_Client();
 $client->setApplicationName('');  

  $client->setClientId(''); // ★(2) ClientId
  $client->setClientSecret(''); // ★(3) ClinetSecret
  $client->setRedirectUri('');// ★(4) RedirectURL
  //$client->setDeveloperKey(''); // ★ (5) なくても大丈夫
  $client->setScopes(array('https://www.googleapis.com/auth/analytics.readonly')); 

  // Magic. Returns objects from the Analytics Service instead of associative arrays.
  $client->setUseObjects(true);


  if (isset($_GET['code'])) {
    //認証の実行
    $client->authenticate();
    $_SESSION['token'] = $client->getAccessToken();
    $redirect = 'http://' . $_SERVER['HTTP_HOST'] . $_SERVER['PHP_SELF'];
    header('Location: ' . filter_var($redirect, FILTER_SANITIZE_URL));
  }
  if (isset($_SESSION['token'])) {
    $client->setAccessToken($_SESSION['token']);
  }

  
  if (!$client->getAccessToken()) {
    
    $authUrl = $client->createAuthUrl();
    print "<a class='login' href='$authUrl'>Connect Me!</a>";
    exit();
  } else {
    // Create analytics service object. See next step below.
    
  }

  $analytics = new Google_AnalyticsService($client); //★ Analytics Service Objectの作成

  runMainDemo($analytics);//クエリーの発行 下に関数を定義


  /* クエリーを発行して結果を出力する関数 */
  function runMainDemo(&$analytics) {
    try {

      // Step 2. Get the user's first view (profile) ID.
      $profileId='';  // ★(7) プロファイル(ビュー)ID
       
      if (isset($profileId)) {

        // Step 3. Query the Core Reporting API.
        $results = getResults($analytics, $profileId);

        // Step 4. Output the results.
        var_dump($results);

      }

    } catch (apiServiceException $e) {
      // Error from the API.
      print 'There was an API error : ' . $e->getCode() . ' : ' . $e->getMessage();

    } catch (Exception $e) {
      print 'There wan a general error : ' . $e->getMessage();
    }
  } 

 /* クエリーを発行してデータ取得する関数 */
  function getResults(&$analytics, $profileId) {
      $optParams = array(
        'dimensions'  => 'ga:pageTitle,ga:pagePath',
        'sort'        => '-ga:visits',
        'max-results' => '25');

     return $analytics->data_ga->get(
         'ga:' . $profileId, //ids 必須
         '2013-06-03',       //start-date 必須
         '2013-08-03',       //end-date 必須
         'ga:visits',        //metrics  必須
         $optParams
         );
  }
?>

<?php

function getProperties() {
    $json = file_get_contents(__DIR__ . '/../data/properties.json');
    return json_decode($json, true);
}

function getResidentialComplexes() {
    $json = file_get_contents(__DIR__ . '/../data/residential_complexes.json');
    return json_decode($json, true);
}

function getPropertyById($id) {
    $properties = getProperties();
    foreach ($properties as $property) {
        if ($property['id'] == $id) {
            return $property;
        }
    }
    return null;
}

function getResidentialComplexById($id) {
    $complexes = getResidentialComplexes();
    foreach ($complexes as $complex) {
        if ($complex['id'] == $id) {
            return $complex;
        }
    }
    return null;
}

function getFilteredProperties($filters = []) {
    $properties = getProperties();
    $filtered = [];

    foreach ($properties as $property) {
        $include = true;

        // Search filter
        if (!empty($filters['search'])) {
            $search = strtolower($filters['search']);
            $searchFields = [
                strtolower($property['title']),
                strtolower($property['developer']),
                strtolower($property['district']),
                strtolower($property['address'])
            ];
            
            $found = false;
            foreach ($searchFields as $field) {
                if (strpos($field, $search) !== false) {
                    $found = true;
                    break;
                }
            }
            
            if (!$found) {
                $include = false;
            }
        }

        // Price filters
        if (!empty($filters['min_price']) && $property['price'] < $filters['min_price']) {
            $include = false;
        }
        
        if (!empty($filters['max_price']) && $property['price'] > $filters['max_price']) {
            $include = false;
        }

        // Developer filter
        if (!empty($filters['developer']) && $property['developer'] !== $filters['developer']) {
            $include = false;
        }

        // District filter
        if (!empty($filters['district']) && $property['district'] !== $filters['district']) {
            $include = false;
        }

        // Rooms filter
        if (!empty($filters['rooms'])) {
            if ($filters['rooms'] === '4+') {
                if ($property['rooms'] < 4) {
                    $include = false;
                }
            } else {
                if ($property['rooms'] != $filters['rooms']) {
                    $include = false;
                }
            }
        }

        // Completion date filter
        if (!empty($filters['completion_date'])) {
            if ($property['completion_year'] > $filters['completion_date']) {
                $include = false;
            }
        }

        // Mortgage filter
        if (!empty($filters['mortgage'])) {
            if ($filters['mortgage'] === 'yes' && !$property['mortgage_available']) {
                $include = false;
            }
            if ($filters['mortgage'] === 'no' && $property['mortgage_available']) {
                $include = false;
            }
        }

        if ($include) {
            $filtered[] = $property;
        }
    }

    return $filtered;
}

function getDevelopers() {
    $properties = getProperties();
    $developers = [];
    
    foreach ($properties as $property) {
        if (!in_array($property['developer'], $developers)) {
            $developers[] = $property['developer'];
        }
    }
    
    sort($developers);
    return $developers;
}

function getDistricts() {
    $properties = getProperties();
    $districts = [];
    
    foreach ($properties as $property) {
        if (!in_array($property['district'], $districts)) {
            $districts[] = $property['district'];
        }
    }
    
    sort($districts);
    return $districts;
}

function formatPrice($price) {
    return number_format($price, 0, ',', ' ') . ' ₽';
}

function calculateCashback($price, $rate = 2.5) {
    return round($price * $rate / 100);
}
?>
